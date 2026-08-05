package com.cvplatform.resume.domain.section;

/**
 * {@code hidePhone}/{@code hideEmail}/{@code hideLocation} let the owner hide
 * individual contact fields on the public page without hiding the whole
 * section - masking is applied when the publish snapshot is built (see
 * {@code StructuredSnapshotBuilder}), not at read time.
 */
public record PersonalInfoContent(
        String fullName,
        String headline,
        String email,
        String phone,
        String location,
        String website,
        boolean hidePhone,
        boolean hideEmail,
        boolean hideLocation) implements SectionContent {
}
