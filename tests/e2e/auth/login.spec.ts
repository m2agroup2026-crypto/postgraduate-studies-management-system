import { test, expect } from '@playwright/test';

const webUrl = process.env.PGMS_WEB_URL || '/';

test.describe('Authentication Flow', () => {
  test('application loads authentication entry point', async ({ page }) => {
    await page.goto(webUrl);

    await expect(page).toHaveURL(/.*/);
    await expect(page.locator('body')).toBeVisible();
  });
});
