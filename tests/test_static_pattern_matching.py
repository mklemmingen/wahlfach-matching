#!/usr/bin/env python3

# Test script to verify static course pattern matching

from src.wahlfach_matching.cache import StaticCourseCache
from src.wahlfach_matching.models import StaticCourse, TimeSlot
from src.wahlfach_matching.optimizer import _load_static_courses
from src.wahlfach_matching.config import MatchConfig
from datetime import time
import os

# Create test directory
os.makedirs('../output/.cache', exist_ok=True)

# Create test static courses
cache = StaticCourseCache('../output/.cache')

must_have_course = StaticCourse(
    code='TEST_MUST',
    name='Test Must Have Course',
    category='must_have',
    schedule=[TimeSlot('Monday', time(10, 0), time(12, 0))]
)

nice_to_have_course = StaticCourse(
    code='TEST_NICE',
    name='Test Nice To Have Course',
    category='nice_to_have',
    schedule=[TimeSlot('Tuesday', time(14, 0), time(16, 0))]
)

cache.save(must_have_course)
cache.save(nice_to_have_course)

print('✓ Created test static courses')
print(f'Must-have: {must_have_course.code} -> {must_have_course.category}')
print(f'Nice-to-have: {nice_to_have_course.code} -> {nice_to_have_course.category}')

# Test the pattern matching integration
config = MatchConfig()
dummy_subjects = {}  # Empty for testing category mapping

static_subjects, static_categories = _load_static_courses(config, dummy_subjects)

print('\n✓ Loaded static courses for pattern matching:')
for code, category in static_categories.items():
    print(f'  {code} -> {category}')

print('\n✓ Verification complete!')
