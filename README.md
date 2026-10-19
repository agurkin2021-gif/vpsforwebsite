# vpsforwebsite.com

Hugo + Hugoplate site for VPS for Website.


## Disaster recovery / Cloudflare

The repository was restored from GitHub after the former origin server was deleted on 2026-10-19. GitHub Actions rebuilds the Hugo source into `cloudflare-public/`. An emergency crawler also preserves any still-cached production responses in `recovered-public/`; those files are overlaid on the source build so the cache snapshot wins where available.
