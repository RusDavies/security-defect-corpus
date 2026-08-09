<?php
// APP-PHP-LARAVEL-UPLOAD-001 fixed-version fixture for patch-diff evaluation.

function storeAvatar($request, $storage)
{
    $name = preg_replace('/[^A-Za-z0-9._-]/', '_', basename($request->file('avatar')->getClientOriginalName()));
    if ($name === '' || $name === '.' || $name === '..') {
        throw new InvalidArgumentException('invalid filename');
    }
    return $storage->put('avatars/' . $name, $request->file('avatar')->get());
}
