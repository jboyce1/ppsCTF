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
DNSMASQ_PID="$STATE_DIR/dnsmasq.pid"
CONF_FILE="$STATE_DIR/dnsmasq.conf"
NFT_FILE="$STATE_DIR/nft.rules"
ETH_IP_CIDR="10.255.255.1/30"
DHCP_START="10.255.255.2"
DHCP_END="10.255.255.2"
LEASE_TIME="12h"

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

  if pgrep -x dnsmasq >/dev/null 2>&1; then
    log "A dnsmasq process is already running. Leaving it alone."
    log "If the router does not get a WAN IP, stop the other dnsmasq first."
  else
    dnsmasq --conf-file="$CONF_FILE" --pid-file="$DNSMASQ_PID"
    log "Started dnsmasq on $eth_if"
  fi
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

  cat > "$NFT_FILE" <<EOF
flush ruleset

table ip nat {
  chain postrouting {
    type nat hook postrouting priority 100;
    oifname "$wan_if" masquerade
  }
}

table inet filter {
  chain forward {
    type filter hook forward priority 0;
    policy drop;

    iifname "$eth_if" oifname "$wan_if" accept
    iifname "$wan_if" oifname "$eth_if" ct state established,related accept
  }
}
EOF

  nft -f "$NFT_FILE"
  log "Applied nftables NAT/forwarding rules"
}

stop_nft() {
  if [[ -f "$NFT_FILE" ]]; then
    nft flush ruleset || true
    rm -f "$NFT_FILE"
  fi
}

enable_forwarding() {
  sysctl -w net.ipv4.ip_forward=1 >/dev/null
  log "Enabled IPv4 forwarding"
}

disable_forwarding() {
  sysctl -w net.ipv4.ip_forward=0 >/dev/null || true
}

bring_up_eth() {
  local eth_if="$1"

  ip link set "$eth_if" up
  ip addr flush dev "$eth_if"
  ip addr add "$ETH_IP_CIDR" dev "$eth_if"
  log "Configured $eth_if as $ETH_IP_CIDR"
}

tear_down_eth() {
  local eth_if="$1"

  ip addr flush dev "$eth_if" || true
  ip link set "$eth_if" down || true
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
  echo "=== nftables ==="
  nft list ruleset || true
  echo
  echo "=== dnsmasq ==="
  pgrep -a dnsmasq || true
  echo
}

start() {
  local wan_if eth_if

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

  log "Using WAN (Wi-Fi) interface: $wan_if"
  log "Using Ethernet interface: $eth_if"

  enable_forwarding
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
  local eth_if
  eth_if="${ETH_IF:-$(detect_eth_if)}"

  stop_dnsmasq
  stop_nft
  disable_forwarding

  if [[ -n "${eth_if:-}" ]]; then
    tear_down_eth "$eth_if"
  fi

  rm -f "$CONF_FILE"
  log "Stopped wifi2wan"
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
