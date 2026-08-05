package com.cvplatform.resume.domain.section;

import com.cvplatform.resume.domain.SectionType;
import java.util.Map;

/** Maps each {@link SectionType} to the Java shape its {@code content_json} must match. */
public final class SectionContentType {

    private static final Map<SectionType, Class<? extends SectionContent>> REGISTRY = Map.ofEntries(
            Map.entry(SectionType.PERSONAL_INFO, PersonalInfoContent.class),
            Map.entry(SectionType.SUMMARY, SummaryContent.class),
            Map.entry(SectionType.SKILLS, SkillsContent.class),
            Map.entry(SectionType.EXPERIENCE, ExperienceContent.class),
            Map.entry(SectionType.PROJECTS, ProjectsContent.class),
            Map.entry(SectionType.EDUCATION, EducationContent.class),
            Map.entry(SectionType.LANGUAGES, LanguagesContent.class),
            Map.entry(SectionType.CERTIFICATIONS, CertificationsContent.class),
            Map.entry(SectionType.LINKS, LinksContent.class),
            Map.entry(SectionType.ADDITIONAL, AdditionalContent.class));

    private SectionContentType() {
    }

    public static Class<? extends SectionContent> classFor(SectionType type) {
        Class<? extends SectionContent> clazz = REGISTRY.get(type);
        if (clazz == null) {
            throw new IllegalArgumentException("No content type registered for " + type);
        }
        return clazz;
    }
}
