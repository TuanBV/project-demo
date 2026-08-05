package com.cvplatform.resume.application;

import java.text.Normalizer;
import java.util.Locale;

/**
 * Cosmetic/SEO slug for public URLs - not required to be globally unique.
 * See docs/architecture.md for why the public link's real identity is
 * {@code publicId}, not the slug.
 */
public final class Slugs {

    private Slugs() {
    }

    public static String slugify(String input) {
        String normalized = Normalizer.normalize(input, Normalizer.Form.NFD)
                .replaceAll("[\\p{InCombiningDiacriticalMarks}]", "");
        String slug = normalized.toLowerCase(Locale.ROOT)
                .replaceAll("[^a-z0-9]+", "-")
                .replaceAll("^-+|-+$", "");
        return slug.isEmpty() ? "cv" : slug;
    }
}
