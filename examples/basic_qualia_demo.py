"""
Basic Qualia Demo

Примеры использования Qualia-as-Evolutionary-Interface.
Демонстрирует базовый цикл: Стимул → Квалиа → Поведение → Исход → Обратная связь

Автор: Kris Stern
Лицензия: MIT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qualia_interface import QualiaInterface, Qualia, Behavior, Outcome
from qualia_metrics import QualiaMetrics
import time


def demo_basic_qualia_generation():
    """Демонстрация 1: Базовая генерация квалиа."""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ 1: Базовая генерация квалиа")
    print("=" * 70)
    
    qi = QualiaInterface()
    
    # Стимул 1: Положительный (еда)
    stimulus_food = {
        'type': 'sensory',
        'modality': 'taste',
        'intensity': 0.8,
        'valence': 'positive',
        'data': {
            'sweetness': 0.9,
            'saltiness': 0.1,
            'texture': 'smooth'
        }
    }
    
    print("\n📥 СТИМУЛ 1: Вкусовой (еда)")
    print(f"  Модальность: {stimulus_food['modality']}")
    print(f"  Интенсивность: {stimulus_food['intensity']}")
    print(f"  Валентность: {stimulus_food['valence']}")
    
    # Генерация квалиа
    qualia_food = qi.generate_qualia(stimulus_food)
    
    print(f"\n🧠 КВАЛИА 1:")
    print(f"  ID: {qualia_food.id[:16]}...")
    print(f"  Timestamp: {qualia_food.timestamp:.3f}")
    print(f"  Интенсивность: {qualia_food.intensity:.4f}")
    print(f"  Валентность: {qualia_food.valence}")
    print(f"  Модальность: {qualia_food.modality}")
    print(f"  Содержание: {len(qualia_food.content['processed_features'])} признаков")
    
    # Стимул 2: Отрицательный (боль)
    stimulus_pain = {
        'type': 'sensory',
        'modality': 'touch',
        'intensity': 0.9,
        'valence': 'negative',
        'data': {
            'temperature': 45,
            'pressure': 0.8,
            'location': 'finger'
        }
    }
    
    print("\n📥 СТИМУЛ 2: Тактильный (боль)")
    print(f"  Модальность: {stimulus_pain['modality']}")
    print(f"  Интенсивность: {stimulus_pain['intensity']}")
    print(f"  Валентность: {stimulus_pain['valence']}")
    
    qualia_pain = qi.generate_qualia(stimulus_pain)
    
    print(f"\n🧠 КВАЛИА 2:")
    print(f"  ID: {qualia_pain.id[:16]}...")
    print(f"  Интенсивность: {qualia_pain.intensity:.4f}")
    print(f"  Валентность: {qualia_pain.valence}")
    print(f"  Модальность: {qualia_pain.modality}")
    
    print("\n✅ Демонстрация 1 завершена")
    print(f"  Сгенерировано квалиа: 2")
    print(f"  Уникальные ID: {qualia_food.id != qualia_pain.id}")
    print()


def demo_behavior_generation():
    """Демонстрация 2: Генерация поведения."""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ 2: Генерация поведения из квалиа")
    print("=" * 70)
    
    qi = QualiaInterface()
    
    # Положительное квалиа
    qualia_positive = {
        'id': 'demo_pos_001',
        'timestamp': time.time(),
        'intensity': 0.8,
        'valence': 'positive',
        'content': {'modality': 'visual', 'quality': 'beautiful'},
        'modality': 'visual'
    }
    
    print("\n🧠 КВАЛИА: Положительное (визуальное)")
    print(f"  Валентность: {qualia_positive['valence']}")
    print(f"  Интенсивность: {qualia_positive['intensity']}")
    
    # Генерация поведения
    behavior = qi.generate_behavior(qualia_positive)
    
    print(f"\n🎯 ПОВЕДЕНИЕ:")
    print(f"  Действие: {behavior.action}")
    print(f"  Направление: {behavior.direction}")
    print(f"  Магнитуда: {behavior.magnitude:.4f}")
    
    # Отрицательное квалиа
    qualia_negative = {
        'id': 'demo_neg_001',
        'timestamp': time.time(),
        'intensity': 0.9,
        'valence': 'negative',
        'content': {'modality': 'auditory', 'quality': 'loud_noise'},
        'modality': 'auditory'
    }
    
    print("\n🧠 КВАЛИА: Отрицательное (аудиальное)")
    print(f"  Валентность: {qualia_negative['valence']}")
    print(f"  Интенсивность: {qualia_negative['intensity']}")
    
    behavior_neg = qi.generate_behavior(qualia_negative)
    
    print(f"\n🎯 ПОВЕДЕНИЕ:")
    print(f"  Действие: {behavior_neg.action}")
    print(f"  Направление: {behavior_neg.direction}")
    print(f"  Магнитуда: {behavior_neg.magnitude:.4f}")
    
    print("\n✅ Демонстрация 2 завершена")
    print(f"  Положительное → {behavior.direction}")
    print(f"  Отрицательное → {behavior_neg.direction}")
    print()


def demo_evolutionary_cycle():
    """Демонстрация 3: Полный эволюционный цикл."""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ 3: Полный эволюционный цикл (50 итераций)")
    print("=" * 70)
    
    import random
    
    qi = QualiaInterface(learning_rate=0.1)
    
    print("\n🔄 Запуск эволюционного цикла...")
    
    success_count = 0
    for cycle in range(50):
        # Генерация случайного стимула
        stimulus = {
            'type': 'sensory',
            'modality': random.choice(['visual', 'auditory', 'touch']),
            'intensity': random.uniform(0.3, 0.9),
            'valence': random.choice(['positive', 'negative', 'neutral']),
            'data': {'cycle': cycle}
        }
        
        # Полный цикл
        qualia = qi.generate_qualia(stimulus)
        behavior = qi.generate_behavior(qualia)
        outcome = qi.evaluate_outcome(behavior, stimulus)
        qi.apply_feedback(outcome)
        
        if cycle < 10 or cycle % 10 == 0:
            print(f"  Цикл {cycle:2d}: {stimulus['modality']:8s} | "
                  f"{stimulus['valence']:9s} → {behavior.direction:8s} | "
                  f"Success: {outcome.success} | "
                  f"Feedback: {outcome.feedback_strength:.4f}")
        
        if outcome.success:
            success_count += 1
    
    # Сохранение в память
    for qualia in qi.memory[:10]:
        qi.store_in_memory(qualia)
    
    print("\n📊 РЕЗУЛЬТАТЫ:")
    print(f"  Всего циклов: 50")
    print(f"  Успешных исходов: {success_count} ({success_count/50*100:.1f}%)")
    print(f"  Записей в памяти: {len(qi.memory)}")
    print(f"  Записей обратной связи: {len(qi.feedback_history)}")
    print(f"  Состояние адаптации: {dict(qi.adaptation_state)}")
    
    # Анализ адаптации
    if len(qi.feedback_history) >= 20:
        first_10 = [o.success for o in qi.feedback_history[:10]]
        last_10 = [o.success for o in qi.feedback_history[-10:]]
        
        first_success = sum(first_10) / len(first_10)
        last_success = sum(last_10) / len(last_10)
        
        print(f"\n📈 АДАПТАЦИЯ:")
        print(f"  Успешность (первые 10): {first_success*100:.1f}%")
        print(f"  Успешность (последние 10): {last_success*100:.1f}%")
        print(f"  Изменение: {((last_success - first_success)*100):+.1f}%")
    
    print("\n✅ Демонстрация 3 завершена")
    print()


def demo_qualia_metrics():
    """Демонстрация 4: Метрики квалиа."""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ 4: Количественные метрики квалиа")
    print("=" * 70)
    
    qi = QualiaInterface()
    
    # Простое квалиа
    qualia_simple = qi.generate_qualia({
        'type': 'sensory',
        'modality': 'visual',
        'intensity': 0.5,
        'valence': 'neutral',
        'data': {'color': 'red'}
    })
    
    # Сложное квалиа
    qualia_complex = qi.generate_qualia({
        'type': 'sensory',
        'modality': 'multimodal',
        'intensity': 0.9,
        'valence': 'positive',
        'data': {
            'visual': {'color': 'rainbow', 'pattern': 'spiral'},
            'auditory': {'tone': 'chord', 'harmony': 'major'},
            'emotional': {'joy': 0.8, 'surprise': 0.6}
        }
    })
    
    print("\n📊 МЕТРИКИ ПРОСТОГО КВАЛИА:")
    metrics_simple = QualiaMetrics.calculate(qualia_simple)
    for key, value in metrics_simple.items():
        print(f"  {key:25s}: {value:.4f}")
    
    print("\n📊 МЕТРИКИ СЛОЖНОГО КВАЛИА:")
    metrics_complex = QualiaMetrics.calculate(qualia_complex)
    for key, value in metrics_complex.items():
        print(f"  {key:25s}: {value:.4f}")
    
    # Сравнение
    comparison = QualiaMetrics.compare(qualia_simple, qualia_complex)
    
    print("\n📊 СРАВНЕНИЕ:")
    for key, value in comparison.items():
        print(f"  {key:25s}: {value:.4f}")
    
    print("\n✅ Демонстрация 4 завершена")
    print(f"  Сложность (простое): {metrics_simple['complexity_score']:.4f}")
    print(f"  Сложность (сложное): {metrics_complex['complexity_score']:.4f}")
    print(f"  Similarity: {comparison['similarity_score']:.4f}")
    print()


def demo_memory_integration():
    """Демонстрация 5: Интеграция с памятью."""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ 5: Интеграция с памятью и поиск")
    print("=" * 70)
    
    qi = QualiaInterface(memory_influence_enabled=True)
    
    print("\n💾 Сохранение квалиа в память...")
    
    # Создаём серию квалиа
    colors = ['red', 'blue', 'green', 'yellow', 'purple']
    for i, color in enumerate(colors):
        qualia = qi.generate_qualia({
            'type': 'sensory',
            'modality': 'visual',
            'intensity': 0.6 + i * 0.05,
            'valence': 'positive',
            'data': {'color': color, 'brightness': 0.7}
        })
        qi.store_in_memory(qualia)
        print(f"  Сохранено: {color:8s} | Intensity: {qualia.intensity:.4f}")
    
    print(f"\n📚 Размер памяти: {len(qi.memory)} квалиа")
    
    # Поиск
    print("\n🔍 Поиск по цвету 'red'...")
    results = qi.search_memory({'color': 'red'})
    print(f"  Найдено: {len(results)} квалиа")
    
    # Влияние памяти на новое квалиа
    print("\n🔄 Генерация нового квалиа с влиянием памяти...")
    new_qualia = qi.generate_qualia({
        'type': 'sensory',
        'modality': 'visual',
        'intensity': 0.6,
        'valence': 'positive',
        'data': {'color': 'red'}
    })
    
    if new_qualia.memory_influence:
        print(f"  Влияние памяти: {new_qualia.memory_influence}")
        print(f"  Intensity modifier: {new_qualia.memory_influence.get('intensity_modifier', 1.0):.4f}")
    
    print("\n✅ Демонстрация 5 завершена")
    print()


def main():
    """Запуск всех демонстраций."""
    print("\n" + "=" * 70)
    print("QUALIA AS EVOLUTIONARY INTERFACE - DEMO")
    print("Функциональная модель квалиа")
    print("=" * 70 + "\n")
    
    demo_basic_qualia_generation()
    time.sleep(1)
    
    demo_behavior_generation()
    time.sleep(1)
    
    demo_evolutionary_cycle()
    time.sleep(1)
    
    demo_qualia_metrics()
    time.sleep(1)
    
    demo_memory_integration()
    
    print("=" * 70)
    print("ВСЕ ДЕМОНСТРАЦИИ ЗАВЕРШЕНЫ")
    print("=" * 70)
    print("\n📚 Документация: README.md")
    print("🧪 Тесты: pytest tests/ -v")
    print("🔬 Исследование: consciousness-research repository")
    print()


if __name__ == '__main__':
    main()
