package com.cvplatform.identity.application;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

/**
 * Local/dev stand-in for a real mail provider: writes the reset link to the
 * application log instead of sending an email. Never logs the raw token
 * anywhere except this line, which only exists so a developer running the
 * app locally can complete the forgot-password flow without an SMTP server.
 */
@Component
public class LoggingNotificationMailer implements NotificationMailer {

    private static final Logger log = LoggerFactory.getLogger(LoggingNotificationMailer.class);

    @Override
    public void sendPasswordResetEmail(String toEmail, String resetLink) {
        log.info("[simulated email] Password reset requested for {}. Reset link: {}", toEmail, resetLink);
    }
}
