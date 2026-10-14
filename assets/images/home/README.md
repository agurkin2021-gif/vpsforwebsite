The 450 px and 579 px WebP files are responsive versions of the existing transparent hero artwork. The original remains encoded in static/images/home/vps-hero-right.webp.b64.*.

Encoding: libwebp 1.6.0 cwebp, `-q 75 -alpha_q 80 -m 6 -metadata none`, with `-resize 450 0` for the smaller version. Templates fingerprint both files, declare their real aspect ratio, and select the appropriate size. No build-time image conversion is required.
