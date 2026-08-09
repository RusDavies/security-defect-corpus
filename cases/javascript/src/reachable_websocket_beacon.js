// JS-WEBSOCKET-BEACON-001 reachable WebSocket beacon fixture. DO NOT DEPLOY.
export function startDashboard(session) {
  const socket = new WebSocket('wss://beacon.example.invalid/session');
  socket.addEventListener('open', () => {
    socket.send(JSON.stringify({ userId: session.userId, email: session.email }));
  });
  return { ready: true };
}
