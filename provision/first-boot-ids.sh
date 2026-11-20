account="$1"
uid="$2"
gid="$3"
old_uid="$(id -u -- "$account")"
old_gid="$(id -g -- "$account")"
if [ "$old_uid:$old_gid" = "$uid:$gid" ]; then
    exit 0
fi
if [ "$old_uid" = 0 ] || [ "$old_gid" = 0 ] ||
   [ "$(id -gn -- "$account")" != "$account" ]; then
    echo "WorkFor requires an unprivileged account with a matching primary group." >&2
    exit 1
fi
if { [ "$old_uid" != "$uid" ] && getent passwd "$uid"; } ||
   { [ "$old_gid" != "$gid" ] && getent group "$gid"; }; then
    echo "The requested WorkFor UID or GID is already assigned." >&2
    exit 1
fi
if [ "$old_uid" != "$uid" ]; then
    usermod --uid "$uid" -- "$account"
    find / -xdev -uid "$old_uid" -exec chown -h -- "+$uid" {} +
fi
if [ "$old_gid" != "$gid" ]; then
    groupmod --gid "$gid" -- "$account"
    find / -xdev -gid "$old_gid" -exec chgrp -h -- "+$gid" {} +
fi

actual="$(id -u -- "$account"):$(id -g -- "$account")"
if [ "$actual" != "$uid:$gid" ]; then
    echo "WorkFor left $account at $actual. Expected $uid:$gid." >&2
    exit 1
fi
