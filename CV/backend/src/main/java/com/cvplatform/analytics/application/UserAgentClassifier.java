package com.cvplatform.analytics.application;

import com.cvplatform.analytics.domain.DeviceType;
import java.util.Locale;
import org.springframework.stereotype.Component;

/**
 * Coarse device-type heuristic from the User-Agent string. Deliberately not
 * a full UA-parsing library - MVP analytics only needs a rough bucket, not
 * precise browser/OS detection.
 */
@Component
public class UserAgentClassifier {

    public DeviceType classify(String userAgent) {
        if (userAgent == null || userAgent.isBlank()) {
            return DeviceType.UNKNOWN;
        }
        String ua = userAgent.toLowerCase(Locale.ROOT);
        if (ua.contains("bot") || ua.contains("crawler") || ua.contains("spider") || ua.contains("facebookexternalhit")
                || ua.contains("linkedinbot") || ua.contains("zalo") || ua.contains("slurp") || ua.contains("preview")) {
            return DeviceType.BOT;
        }
        if (ua.contains("ipad") || ua.contains("tablet") || (ua.contains("android") && !ua.contains("mobile"))) {
            return DeviceType.TABLET;
        }
        if (ua.contains("mobi") || ua.contains("iphone") || ua.contains("android")) {
            return DeviceType.MOBILE;
        }
        return DeviceType.DESKTOP;
    }
}
