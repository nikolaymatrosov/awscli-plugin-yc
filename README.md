awscli-plugin-yc
=============

This awscli plugin provides service endpoint configuration and auth via service account in Yandex Cloud.


------------
Installation
------------

The easiest way to install awscli-plugin-yc is to use `pip`:

    $ pip install awscli-plugin-yc

You can also install the latest package from GitHub source which can contain changes not yet pushed to PyPI:

    $ pip install git+https://github.com/nikolaymatrosov/awscli-plugin-yc.git

or, if you install `awscli` via Homebrew, which bundles its own python, install as following:

    $ /usr/local/opt/awscli/libexec/bin/pip install awscli-plugin-yc

Regardless of the installation method, make note of the package installation path (e.g. `~/Library/Python/3.7/lib/python/site-packages`). It will be needed if you are using AWS CLI v2.

---------------
Getting Started
---------------

Before using awscli-plugin-yc plugin, you need to [configure awscli](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) first.

**MUST**: Once that's done, to enable `awscli-plugin-yc` plugin, you can run:

    $ aws configure set plugins.yc awscli_plugin_yc

The above command adds below section to your aws config file. You can also directly edit your `~/.aws/config` with below configuration.

    [plugins]
    yc = awscli_plugin_yc

If you are configuring AWS CLI v2 to use the yc plugin, you will need to add an additional configuration setting, replacing "site-packages-path" with the installation path noted above:

    $ aws configure set plugins.cli_legacy_plugin_path site-packages-path

The configuration file will now have two values in the plugin section:

    [plugins]
    yc = awscli_plugin_yc
    cli_legacy_plugin_path = site-packages-path
