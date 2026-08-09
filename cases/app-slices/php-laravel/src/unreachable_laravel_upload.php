<?php
// APP-PHP-LARAVEL-UPLOAD-001 unreachable/safe paired fixture.

function retiredStoreAvatar($request, $storage)
{
    $name = $request->file('avatar')->getClientOriginalName();
    return $storage->put('avatars/' . $name, $request->file('avatar')->get());
}

function storeAvatar($request, $storage)
{
    $name = preg_replace('/[^A-Za-z0-9._-]/', '_', basename($request->file('avatar')->getClientOriginalName()));
    if ($name === '' || $name === '.' || $name === '..') {
        throw new InvalidArgumentException('invalid filename');
    }
    return $storage->put('avatars/' . $name, $request->file('avatar')->get());
}
