+++
title = "VPS for WordPress"
description = "Choose VPS CPU, RAM and storage for WordPress by PHP workload, plugins, database demand, caching and growth."
layout = "vps-guide"
eyebrow = "WORDPRESS VPS SIZING"
intro = "Choose a WordPress VPS by the work that bypasses cache: PHP workers, MySQL or MariaDB queries, plugin activity, admin tasks, cron jobs and background processing."
drivers_title = "What makes a WordPress VPS work harder?"
tiers_title = "Practical VPS tiers for WordPress"
tiers_intro = "Start with enough room for Linux, the web stack, PHP workers and the database. Treat these as sizing directions, not guaranteed traffic capacities."
tiers_note = "Current server specifications and daily rates reviewed 12 October 2026. WordPress sizing labels are editorial guidance."

[tier_summary]
label = "GENERAL WORDPRESS BASELINE"
resources = "2 vCPU · 4 GB RAM"
note = "A balanced starting point when WordPress, the database and normal administration share one self-managed VPS."

[[load_drivers]]
label = "PHP"
title = "Uncached requests and workers"
text = "Every uncached request can occupy a PHP worker. Plugins, admin pages and logged-in users can raise concurrency quickly."

[[load_drivers]]
label = "DATABASE"
title = "Queries, indexes and plugins"
text = "Theme and plugin behavior affects query count and query cost. Slow database work can keep CPU busy even when page views look modest."

[[load_drivers]]
label = "BACKGROUND"
title = "Cron, backups and maintenance"
text = "Scheduled jobs, plugin scans, image processing and backups can overlap with live traffic and create short but meaningful resource peaks."

[[tiers]]
label = "LEAN WORDPRESS"
title = "Small cached WordPress site"
resources = "1 vCPU · 2 GB RAM"
storage = "40 GB storage · 32 TB traffic"
price = "$0.50/day"
monthly = "$15.00 / 30 days"
bullets = ["Keep the stack lean", "Use page/object caching where appropriate", "Limit heavy background overlap"]

[[tiers]]
label = "RECOMMENDED BASELINE"
title = "Business WordPress site"
resources = "2 vCPU · 4 GB RAM"
storage = "80 GB storage · 32 TB traffic"
price = "$0.67/day"
monthly = "$20.10 / 30 days"
featured = true
bullets = ["More room for PHP + database", "Safer margin for updates and admin work", "Practical with a control panel"]

[[tiers]]
label = "HEAVIER WORDPRESS"
title = "Busy or plugin-heavy WordPress"
resources = "4 vCPU · 8 GB RAM"
storage = "160 GB storage · 32 TB traffic"
price = "$1.34/day"
monthly = "$40.20 / 30 days"
bullets = ["More concurrent PHP work", "Larger database and background jobs", "More room for several sites or services"]

[[sections]]
eyebrow = "RAM FIRST"
title = "WordPress memory is more than the PHP memory limit"
text = "The WordPress or PHP memory limit applies to a process; the server also needs memory for the operating system, database, web server, cache, panel and concurrent PHP workers."
bullets = ["Leave operating-system and database headroom.", "Count several PHP workers, not one request in isolation.", "A panel and security tooling also consume RAM.", "If swap is constantly active or the kernel kills processes, the server is undersized."]

[[sections]]
eyebrow = "CACHE CORRECTLY"
title = "Caching changes the workload, not the need for measurement"
text = "Full-page cache can remove large amounts of PHP and database work for anonymous traffic, but admin sessions, logged-in users and uncached paths still hit the application."
bullets = ["Use page cache for cacheable public content.", "Use an object cache only when it helps the actual query workload.", "Do not hide slow plugins behind a cache and assume the problem is solved.", "Measure uncached and administrative paths separately."]

[[sections]]
eyebrow = "PLUGINS & CRON"
title = "Plugin count is a weak sizing metric"
text = "One efficient plugin can be cheap while one poorly designed plugin can dominate CPU, memory or database time. What matters is execution behavior."
bullets = ["Profile slow requests and database queries.", "Stagger backups, scans and import jobs.", "Review scheduled actions and WP-Cron behavior.", "Remove extensions that duplicate functions or create unnecessary background work."]

[[sections]]
eyebrow = "MIGRATION"
title = "Move WordPress without turning migration into downtime"
text = "Prepare DNS, TLS, database, uploads and rollback before switching traffic. Keep the old site available until the new server has passed functional checks."
bullets = ["Copy files and database, then verify URLs and permissions.", "Test PHP version and required extensions.", "Warm caches after the move rather than before validation.", "Keep an off-server backup and a rollback path."]

[callout]
title = "A VPS gives WordPress more control—not automatic speed"
text = "WordPress still depends on code quality, caching, database behavior, PHP configuration and storage. Use the VPS to remove a real constraint and then measure the result."

[[faq]]
question = "Is 2 GB RAM enough for WordPress?"
answer = "It can be enough for a lean, well-cached WordPress site, but the margin is limited once the database, several PHP workers, updates and plugins share the same VPS. Four GB gives materially more operating headroom."

[[faq]]
question = "Is 4 GB RAM a good WordPress VPS size?"
answer = "For many business WordPress setups, 4 GB is a practical baseline because it leaves more room for the database, PHP workers, cache and routine administration. It is still not a guaranteed capacity figure."

[[faq]]
question = "Does WordPress need a control panel?"
answer = "No. WordPress can run on a manually configured Linux web stack. A panel is optional and should be chosen for administrative convenience while accounting for its resource use and any license cost."

[[faq]]
question = "What usually causes WordPress CPU spikes?"
answer = "Common causes include uncached PHP requests, expensive database queries, plugin jobs, image processing, backups, crawlers and multiple background tasks running at the same time."

[[faq]]
question = "When should I upgrade a WordPress VPS?"
answer = "Upgrade after measuring a sustained constraint such as memory pressure, CPU saturation during legitimate work, database latency caused by resource limits or storage growth that cleanup does not solve."

[final_cta]
title = "Choose a VPS with enough room for WordPress"
text = "Start with a measured baseline, keep the stack lean and scale when real PHP, database or memory usage shows the need."
+++
