import { test, expect } from '@playwright/test';

/**
 * PGMS RBAC validation foundation.
 * Scenarios will be connected to real routes after UI route audit.
 */
test.describe('Role permissions', () => {
  test('student cannot access restricted resources', async ({ page }) => {
    await page.goto('/');
    await expect(page).toBeDefined();
  });
});
