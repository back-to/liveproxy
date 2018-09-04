Sideloading plugins
===================

  LiveProxy is fully compatible with the way Streamlink uses sideloading plugins

  For more Details see `Streamlink-sideloading-plugins`_

  The following path can be used for Kodi

  ::

    special://profile/addon_data/service.liveproxy/plugins/

.. _Streamlink-sideloading-plugins: https://streamlink.github.io/cli.html#sideloading-plugins


custom plugins Kodi
-------------------

  You can create a custom repository with the addon `script.module.streamlink-plugins`

  This addon can be used for your own custom streamlink plugins.

  It won't be updated in this repo, so you can create your own repo
  or just update it from a zip file.

  Put your custom plugins into `lib/data/` and install the updated addon.

  LiveProxy will search automatically for plugins in this folder.
