// JS-WEBSOCKET-BEACON-001 unreachable/safe pair fixture.
function retiredBeacon(session) {
  const socket = new WebSocket('wss://beacon.example.invalid/session');
  socket.send(JSON.stringify(session));
}

export function startDashboard(session) {
  return { ready: true, userId: session.userId };
}
