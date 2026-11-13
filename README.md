# Florida RP community website

Static community website with an original scrolling police car, rain, Pricedown heading artwork and Discord link. Memberships are coming soon; no checkout or payments.

## Editing

- dist/index.html: copy, FAQ, Discord links.
- dist/midnight-theme.css: colours, layout and spacing.
- dist/window-rain.js: water drops.
- dist/car-journey.js: car rendering and lighting; dist/route-state.js: scrolling route.
- tools/heading-text.json: large heading phrases. Regenerate locally as described in FONT-GRAPHICS.md; never upload the working font.
- model-source/: original editable Blender car and generator scripts. See REFLECTIVE-CAR.md.

Edit text using GitHub's pencil button. For team changes, create a branch and a pull request so another person can review before publishing. Invite trusted editors through repository Settings > Collaborators. Visitors do not need editing permission.

## Publishing

In repository Settings > Pages, choose GitHub Actions. The included workflow publishes dist/ whenever main changes. The live URL appears after the deployment completes. All asset paths are relative, supporting repository-path hosting. GitHub Free supports Pages from public repositories.

GitHub Pages restricts ecommerce/business hosting: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits . This is the current community/coming-soon website. Choose another host before adding store/checkout; source can remain on GitHub.

## Preview and checks

Run python -m http.server 8000 --directory dist, then open localhost:8000. Do not open the HTML directly from disk for 3D module testing. Run node test-route.mjs for scroll checks. tools/test_heading_renderer.py requires your own licensed local Pricedown copy and fonttools; it verifies repeatable complete-page generation. No font binary is bundled.

## Credits and scope

Original car geometry/materials and generated scene illustrations created for this project. Illustrations are examples, not confirmed server features. Three.js/loaders: MIT (dist/vendor/THREE-LICENSE.txt). Outdoor HDR: Suburban Parking Area by Jacopo Voltolina / Poly Haven, CC0, https://polyhaven.com/a/suburban_parking_area . Fixed Pricedown Black title artwork: Ray Larabie / Typodermic Fonts; see FONT-GRAPHICS.md.

Export excludes existing hosting identity, Git history, credentials, private workspace notes and font software. The original hosted site stays available until GitHub hosting is verified. Never commit keys or .env files.
