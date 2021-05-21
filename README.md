## `notify-when-versionup-action`
This action is for research on self-admitted technical debt on Docker.

The action runs every 24 hours (though it needs to be set by the user ...) and detects commented github issue and release links in the Dockerfile.
If the linked issue is closed or a new version is released within the last 24 hours, we will create a PR to notify the developer.

## detail
* this action need some inputs
  * GITHUB_TOKEN
  * REPOSITORY
  * DEFAULT_BRANCH
* please create `.github/workflows/main.yml` see install example

## install example
.github/workflows/main.yml
```
name: notify-when-versionup-action

on:
  schedule:
    # 毎日 11:00 (JST) に処理を実行する。
    # UTC 02:00 -> JST 11:00
    - cron: '0 2 * * *'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      - name: Notify When VersionUp action
        uses: posl/notify-when-versionup-action@1.1.0
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          REPOSITORY: ${{ github.repository }}
          DEFAULT_BRANCH: ${{ github.ref }}
```
