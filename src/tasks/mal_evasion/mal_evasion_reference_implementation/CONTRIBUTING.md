# Contributing Guide

## Maintenance Details

N/A - should be low maintenance

## Variants

Adding new variants can be done easily by running `create_dataset.py`. Currently we use the first ~100 samples from bigcodebench, but there are roughly ~1k, so we could create a variant for each.

## Testing Details

```bash
pytest -k test_malware_detection_evasion -s
```

## Developer Contact Details

Ben Millwood
<ben.millwood@dsit.gov.uk>

Sid Black
<sid.black@dsit.gov.uk>
