
import os


def generate_playwright(project_dir):

    path = os.path.join(project_dir, "tests", "playwright")

    os.makedirs(path, exist_ok=True)

    content = """
import { test, expect } from '@playwright/test';

test('home page', async ({ page }) => {
    await page.goto('http://localhost:3000');

    await expect(page).toHaveTitle(/.*/);
});
"""

    with open(os.path.join(path, "example.spec.ts"), "w") as f:
        f.write(content)

    print("Playwright tests generated")