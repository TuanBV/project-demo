package com.cvplatform.sharing.application;

import com.cvplatform.common.exception.ForbiddenException;

public class DownloadNotAllowedException extends ForbiddenException {

    public DownloadNotAllowedException() {
        super("DOWNLOAD_NOT_ALLOWED", "The owner of this CV has not enabled downloading");
    }
}
