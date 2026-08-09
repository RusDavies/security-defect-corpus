<?php
// APP-PHP-LARAVEL-UPLOAD-001 reachable vulnerable fixture. DO NOT DEPLOY.

function storeAvatar($request, $storage)
{
    $name = $request->file('avatar')->getClientOriginalName();
    return $storage->put('avatars/' . $name, $request->file('avatar')->get());
}
