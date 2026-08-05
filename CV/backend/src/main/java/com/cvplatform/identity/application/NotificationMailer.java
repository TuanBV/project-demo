package com.cvplatform.identity.application;

/**
 * Abstraction over outbound transactional email so {@link AuthService} never
 * depends on a concrete mail provider. The MVP ships {@link LoggingNotificationMailer};
 * a real SMTP/SES-backed implementation can be swapped in later behind this
 * same interface.
 */
public interface NotificationMailer {

    void sendPasswordResetEmail(String toEmail, String resetLink);
}
