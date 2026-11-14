# PK overview

The two-page overview of PK plus its Technical setup page.

Current: App 2026.11.14 (5031a69), Document 1.1.

Published page: https://claude.ai/artifact/7XTetauea4917zZQV839yi (artifact slug 34d7921a-9866-434f-9344-77669464c7f9)
PDF copy in Google Drive: App Overviews folder, "PK Overview - App 2026.11.14 - Doc 1.1.pdf" (https://drive.google.com/drive/folders/1OlCKC8_z5Kcuee_786cEiDQqrXse1CVd)

## Regenerating

```
PK_CODE=XXXX-XXXX-XXXX-XXXX node docs/overview/shoot.js   # retakes shots/*.png from the locked game
node docs/overview/pdf.js                                  # prints overview.pdf
```

The access code is only read from the environment. The overview uses the JPEG copies in `shots/` (600 px wide) to keep the PDF small; remake them from the PNGs after a reshoot. When the app changes in a way a player would notice, update the captions and sections, bump the document version and the app version on every page footer, republish the artifact above, and replace the PDF in the Drive folder.
