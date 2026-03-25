#!/usr/bin/env bash
set -euo pipefail

# wifi2wan.sh
# Share laptop Wi-Fi -> Ethernet so a router WAN port can get internet through this laptop.
#
# Order of operations matters: 
#     - Connect to internet via wifi first.
#     chmod +x ./wifi2wan.sh
#     sudo ./wifi2wan.sh start
#     plug ethernet into the wan port of router
#
# Commands:
#   sudo ./wifi2wan.sh start
#   sudo ./wifi2wan.sh stop
#   sudo ./wifi2wan.sh status
#
# Default behavior:
# - Wi-Fi interface = auto-detected default route interface
# - Ethernet interface = first non-Wi-Fi ethernet-like interface
# - Laptop Ethernet IP = 10.255.255.1/30
# - Router WAN gets DHCP from dnsmasq on Ethernet
# - NAT handled by nftables
#
STATE_DIR="/run/wifi2wan"
STATE_FILE="$STATE_DIR/state.env"
DNSMASQ_PID="$STATE_DIR/dnsmasq.pid"
CONF_FILE="$STATE_DIR/dnsmasq.conf"

ETH_IP_CIDR="10.255.255.1/30"
DHCP_START="10.255.255.2"
DHCP_END="10.255.255.2"
LEASE_TIME="12h"

NFT_NAT_TABLE="wifi2wan_nat"
NFT_FILTER_TABLE="wifi2wan_filter"

mkdir -p "$STATE_DIR"

log() {
  echo "[*] $*"
}

err() {
  echo "[!] $*" >&2
}

need_root() {
  if [[ "${EUID}" -ne 0 ]]; then
    err "Run as root: sudo $0 <start|stop|status>"
    exit 1
  fi
}

detect_wan_if() {
  ip route | awk '/^default/ {print $5; exit}'
}

detect_eth_if() {
  ip -o link show | awk -F': ' '{print $2}' \
    | grep -Ev '^(lo|wl|wlan|virbr|vboxnet|docker|br-|tun|tap)' \
    | head -n 1
}

save_state() {
  local wan_if="$1"
  local eth_if="$2"
  local old_ipfwd="$3"

  cat > "$STATE_FILE" <<EOF
WAN_IF="$wan_if"
ETH_IF="$eth_if"
OLD_IP_FORWARD="$old_ipfwd"
EOF
}

load_state() {
  if [[ -f "$STATE_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$STATE_FILE"
  fi
}

start_dnsmasq() {
  local eth_if="$1"

  cat > "$CONF_FILE" <<EOF
interface=$eth_if
bind-interfaces
dhcp-range=$DHCP_START,$DHCP_END,$LEASE_TIME
dhcp-option=3,10.255.255.1
dhcp-option=6,1.1.1.1,8.8.8.8
port=0
log-dhcp
EOF

  if [[ -f "$DNSMASQ_PID" ]]; then
    local oldpid
    oldpid="$(cat "$DNSMASQ_PID" 2>/dev/null || true)"
    if [[ -n "${oldpid:-}" ]] && kill -0 "$oldpid" 2>/dev/null; then
      log "dnsmasq already running under this script."
      return
    fi
  fi

  dnsmasq --conf-file="$CONF_FILE" --pid-file="$DNSMASQ_PID"
  log "Started dnsmasq on $eth_if"
}

stop_dnsmasq() {
  if [[ -f "$DNSMASQ_PID" ]]; then
    local pid
    pid="$(cat "$DNSMASQ_PID" 2>/dev/null || true)"
    if [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" || true
      sleep 1
    fi
    rm -f "$DNSMASQ_PID"
  fi
}

start_nft() {
  local wan_if="$1"
  local eth_if="$2"

  nft list table ip "$NFT_NAT_TABLE" >/dev/null 2>&1 && nft delete table ip "$NFT_NAT_TABLE" || true
  nft list table inet "$NFT_FILTER_TABLE" >/dev/null 2>&1 && nft delete table inet "$NFT_FILTER_TABLE" || true

  nft add table ip "$NFT_NAT_TABLE"
  nft "add chain ip $NFT_NAT_TABLE postrouting { type nat hook postrouting priority 100; policy accept; }"
  nft add rule ip "$NFT_NAT_TABLE" postrouting oifname "$wan_if" masquerade

  nft add table inet "$NFT_FILTER_TABLE"
  nft "add chain inet $NFT_FILTER_TABLE forward { type filter hook forward priority 0; policy drop; }"
  nft add rule inet "$NFT_FILTER_TABLE" forward iifname "$eth_if" oifname "$wan_if" accept
  nft add rule inet "$NFT_FILTER_TABLE" forward iifname "$wan_if" oifname "$eth_if" ct state established,related accept

  log "Applied nftables NAT/forwarding rules"
}

stop_nft() {
  nft list table ip "$NFT_NAT_TABLE" >/dev/null 2>&1 && nft delete table ip "$NFT_NAT_TABLE" || true
  nft list table inet "$NFT_FILTER_TABLE" >/dev/null 2>&1 && nft delete table inet "$NFT_FILTER_TABLE" || true
}

get_ip_forward() {
  cat /proc/sys/net/ipv4/ip_forward
}

set_ip_forward() {
  local value="$1"
  sysctl -w "net.ipv4.ip_forward=$value" >/dev/null
}

bring_up_eth() {
  local eth_if="$1"

  # Tell NetworkManager to stop managing this interface while we use it
  nmcli device set "$eth_if" managed no >/dev/null 2>&1 || true

  ip link set "$eth_if" up
  ip addr flush dev "$eth_if"
  ip addr add "$ETH_IP_CIDR" dev "$eth_if"

  log "Configured $eth_if as $ETH_IP_CIDR"
}

restore_eth() {
  local eth_if="$1"

  ip addr flush dev "$eth_if" || true
  ip link set "$eth_if" up || true

  # Hand interface back to NetworkManager
  nmcli device set "$eth_if" managed yes >/dev/null 2>&1 || true
  nmcli device connect "$eth_if" >/dev/null 2>&1 || true

  # Fallback for systems without NM or where NM doesn't immediately reconnect
  dhclient -r "$eth_if" >/dev/null 2>&1 || true
  dhclient "$eth_if" >/dev/null 2>&1 || true

  log "Restored $eth_if to normal management"
}

status() {
  echo
  echo "=== Interfaces ==="
  ip -br addr
  echo
  echo "=== Default Route ==="
  ip route | grep '^default' || true
  echo
  echo "=== Forwarding ==="
  sysctl net.ipv4.ip_forward || true
  echo
  echo "=== nftables tables ==="
  nft list table ip "$NFT_NAT_TABLE" 2>/dev/null || true
  nft list table inet "$NFT_FILTER_TABLE" 2>/dev/null || true
  echo
  echo "=== dnsmasq ==="
  pgrep -a dnsmasq || true
  echo
  echo "=== Saved state ==="
  [[ -f "$STATE_FILE" ]] && cat "$STATE_FILE" || true
  echo
}

start() {
  local wan_if eth_if old_ipfwd

  wan_if="${WAN_IF:-$(detect_wan_if)}"
  eth_if="${ETH_IF:-$(detect_eth_if)}"

  if [[ -z "${wan_if:-}" ]]; then
    err "Could not detect Wi-Fi/default-route interface."
    exit 1
  fi

  if [[ -z "${eth_if:-}" ]]; then
    err "Could not detect Ethernet interface."
    exit 1
  fi

  if [[ "$wan_if" == "$eth_if" ]]; then
    err "WAN and Ethernet interfaces resolved to the same device: $wan_if"
    exit 1
  fi

  old_ipfwd="$(get_ip_forward)"

  save_state "$wan_if" "$eth_if" "$old_ipfwd"

  log "Using WAN (Wi-Fi) interface: $wan_if"
  log "Using Ethernet interface: $eth_if"

  set_ip_forward 1
  log "Enabled IPv4 forwarding"

  bring_up_eth "$eth_if"
  start_nft "$wan_if" "$eth_if"
  start_dnsmasq "$eth_if"

  echo
  log "Done."
  log "Plug the laptop Ethernet into the router WAN port."
  log "Router WAN should receive $DHCP_START via DHCP."
  echo
}

stop() {
  load_state

  local eth_if="${ETH_IF:-${ETH_IF:-$(detect_eth_if)}}"
  local old_ipfwd="${OLD_IP_FORWARD:-0}"

  stop_dnsmasq
  stop_nft
  set_ip_forward "$old_ipfwd"

  if [[ -n "${eth_if:-}" ]]; then
    restore_eth "$eth_if"
  fi

  rm -f "$CONF_FILE" "$STATE_FILE"
  log "Stopped wifi2wan and restored normal Ethernet behavior"
}

main() {
  need_root

  case "${1:-}" in
    start) start ;;
    stop) stop ;;
    status) status ;;
    *)
      echo "Usage: sudo $0 {start|stop|status}"
      exit 1
      ;;
  esac
}

main "$@"
