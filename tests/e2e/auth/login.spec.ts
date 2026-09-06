import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('user can login and access dashboard', async ({ page }) => {
    await page.goto('/');

    // TODO: Replace selectors after reviewing the actual web application routes.
    await expect(page).toHaveTitle(/Postgraduate|Studies|Management/i);
  });
});
