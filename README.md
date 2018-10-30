Getting Setup on a New System
=============================

Increase max_user_watches (file handles)
----------------------------------------

Need to do this for:

* [Large Visual Studio Code workspaces](https://code.visualstudio.com/docs/setup/linux#_visual-studio-code-is-unable-to-watch-for-file-changes-in-this-large-workspace-error-enospc)
* [Kubernetes](https://github.com/kubernetes/kubernetes/issues/46230)

How big should it be?  More than the default is all the consensus seems to provide.
[Stackoverflow - What is a reasonable amount of inotify watches with linux?](https://stackoverflow.com/questions/535768/what-is-a-reasonable-amount-of-inotify-watches-with-linux)

Increase the number of fs.inotify.max_user_watches (handles)
https://github.com/guard/listen/wiki/Increasing-the-amount-of-inotify-watchers

```bash
cat /proc/sys/fs/inotify/max_user_watches
# Note -- This is not idempotent, should do something more elegant in the script
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
cat /proc/sys/fs/inotify/max_user_watches
```