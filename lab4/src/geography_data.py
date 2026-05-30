"""Demo thematic data for the geography variant."""

from __future__ import annotations

from src.models import GeographyRecord


def demo_records() -> list[GeographyRecord]:
    return [
        GeographyRecord("Азия", "Самый большой материк Земли."),
        GeographyRecord("Арктика", "Полярная область вокруг Северного полюса."),
        GeographyRecord("Атлантика", "Океан между Европой, Африкой и Америкой."),
        GeographyRecord("Африка", "Материк в восточном полушарии."),
        GeographyRecord("Байкал", "Крупнейшее пресноводное озеро по объему."),
        GeographyRecord("Балтика", "Море Северной Европы."),
        GeographyRecord("Бархан", "Песчаная форма рельефа пустынь."),
        GeographyRecord("Бассейн", "Территория стока реки или водосбора."),
        GeographyRecord("Берингово море", "Море Тихого океана между Азией и Америкой."),
        GeographyRecord("Волга", "Крупнейшая река Европы."),
        GeographyRecord("Гималаи", "Высочайшая горная система Земли."),
        GeographyRecord("Гоби", "Пустыня в Центральной Азии."),
    ]
