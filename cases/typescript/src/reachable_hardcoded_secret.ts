// TS-SECRET-001 reachable hardcoded secret fixture. DO NOT DEPLOY.
export function buildPaymentClient() {
  const apiKey = "sk_live_51HARD_CODED_TEST_SECRET";
  return { apiKey, endpoint: "https://payments.example.test" };
}
