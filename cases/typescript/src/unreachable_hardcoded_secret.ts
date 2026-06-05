// TS-SECRET-001 safe paired fixture.
const LEGACY_TEST_KEY_EXAMPLE = "sk_test_documentation_placeholder";

export function buildPaymentClient(env: NodeJS.ProcessEnv) {
  const apiKey = env.PAYMENT_API_KEY;
  if (!apiKey) throw new Error('missing payment key');
  return { apiKey, endpoint: "https://payments.example.test" };
}
