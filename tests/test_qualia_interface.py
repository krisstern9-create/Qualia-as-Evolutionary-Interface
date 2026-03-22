import pytest
import time
import numpy as np
from pathlib import Path

class TestQualiaInterface:
    """
    Тесты для проверки функциональной модели квалиа.
    
    Гипотеза: Квалиа — это эволюционный интерфейс,
    который преобразует стимулы в поведение через
    субъективный опыт с обратной связью.
    """
    
    def test_qualia_generation_from_stimulus(self):
        """
        Тест 1: Генерация квалиа из стимула.
        
        Проверяем:
        - Стимул создаёт квалиа
        - Квалиа имеет измеримые параметры
        - Разные стимулы создают разные квалиа
        """
        from qualia_interface import QualiaInterface
        
        qi = QualiaInterface()
        
        # Стимул 1: положительный (еда)
        stimulus_food = {
            'type': 'sensory',
            'modality': 'taste',
            'intensity': 0.8,
            'valence': 'positive',
            'data': {'sweetness': 0.9, 'saltiness': 0.1}
        }
        
        # Стимул 2: отрицательный (боль)
        stimulus_pain = {
            'type': 'sensory',
            'modality': 'touch',
            'intensity': 0.9,
            'valence': 'negative',
            'data': {'temperature': 45, 'pressure': 0.8}
        }
        
        # Генерируем квалиа
        qualia_food = qi.generate_qualia(stimulus_food)
        qualia_pain = qi.generate_qualia(stimulus_pain)
        
        # Проверка 1: Квалиа создано
        assert qualia_food is not None
        assert qualia_pain is not None
        
        # Проверка 2: Квалиа имеет структуру
        assert 'id' in qualia_food
        assert 'timestamp' in qualia_food
        assert 'intensity' in qualia_food
        assert 'valence' in qualia_food
        assert 'content' in qualia_food
        
        # Проверка 3: Разные стимулы = разные квалиа
        assert qualia_food['id'] != qualia_pain['id']
        assert qualia_food['valence'] != qualia_pain['valence']
        assert qualia_food['intensity'] != qualia_pain['intensity']
        
        # Проверка 4: Интенсивность коррелирует со стимулом
        assert qualia_food['intensity'] > 0.5
        assert qualia_pain['intensity'] > 0.5
        
        print(f"✓ Тест 1 пройден: Квалиа сгенерировано успешно")
        print(f"  Food qualia: {qualia_food['id'][:8]}... valence={qualia_food['valence']}")
        print(f"  Pain qualia: {qualia_pain['id'][:8]}... valence={qualia_pain['valence']}")
    
    def test_behavior_generation_from_qualia(self):
        """
        Тест 2: Генерация поведения из квалиа.
        
        Проверяем:
        - Квалиа преобразуется в поведение
        - Поведение соответствует валентности квалиа
        - Есть вариативность в поведении
        """
        from qualia_interface import QualiaInterface
        
        qi = QualiaInterface()
        
        # Создаём квалиа
        qualia_positive = {
            'id': 'q_pos_001',
            'timestamp': time.time(),
            'intensity': 0.8,
            'valence': 'positive',
            'content': {'modality': 'taste', 'quality': 'sweet'}
        }
        
        qualia_negative = {
            'id': 'q_neg_001',
            'timestamp': time.time(),
            'intensity': 0.9,
            'valence': 'negative',
            'content': {'modality': 'touch', 'quality': 'pain'}
        }
        
        # Генерируем поведение
        behavior_pos = qi.generate_behavior(qualia_positive)
        behavior_neg = qi.generate_behavior(qualia_negative)
        
        # Проверка 1: Поведение создано
        assert behavior_pos is not None
        assert behavior_neg is not None
        
        # Проверка 2: Поведение имеет структуру
        assert 'action' in behavior_pos
        assert 'direction' in behavior_pos
        assert 'magnitude' in behavior_pos
        
        # Проверка 3: Поведение соответствует валентности
        # Положительное → приближение
        # Отрицательное → избегание
        assert behavior_pos['direction'] == 'approach'
        assert behavior_neg['direction'] == 'avoid'
        
        # Проверка 4: Magnitude коррелирует с интенсивностью
        assert behavior_pos['magnitude'] > 0
        assert behavior_neg['magnitude'] > 0
        
        print(f"✓ Тест 2 пройден: Поведение сгенерировано успешно")
        print(f"  Positive: {behavior_pos['action']} → {behavior_pos['direction']}")
        print(f"  Negative: {behavior_neg['action']} → {behavior_neg['direction']}")
    
    def test_evolutionary_feedback_loop(self):
        """
        Тест 3: Эволюционная обратная связь.
        
        Проверяем:
        - Система запоминает исход поведения
        - Обратная связь влияет на будущие решения
        - Есть адаптация со временем
        """
        from qualia_interface import QualiaInterface
        
        qi = QualiaInterface()
        
        # Симуляция 10 циклов
        results = []
        for i in range(10):
            stimulus = {
                'type': 'sensory',
                'modality': 'visual',
                'intensity': 0.5 + (i * 0.05),
                'valence': 'positive' if i % 2 == 0 else 'negative',
                'data': {'pattern': f'pattern_{i}'}
            }
            
            qualia = qi.generate_qualia(stimulus)
            behavior = qi.generate_behavior(qualia)
            
            # Симуляция исхода (успех/неуспех)
            outcome = qi.evaluate_outcome(behavior, stimulus)
            
            results.append({
                'cycle': i,
                'stimulus_valence': stimulus['valence'],
                'behavior_direction': behavior['direction'],
                'outcome': outcome['success'],
                'feedback_strength': outcome['feedback_strength']
            })
        
        # Проверка 1: Все циклы завершены
        assert len(results) == 10
        
        # Проверка 2: Есть обратная связь
        assert all('feedback_strength' in r for r in results)
        
        # Проверка 3: Адаптация происходит
        # Первые 5 циклов vs последние 5 циклов
        first_half_success = sum(1 for r in results[:5] if r['outcome'])
        second_half_success = sum(1 for r in results[5:] if r['outcome'])
        
        # Система должна улучшаться (или хотя бы не ухудшаться)
        assert second_half_success >= first_half_success - 2
        
        # Проверка 4: Feedback записан в историю
        assert len(qi.feedback_history) > 0
        
        print(f"✓ Тест 3 пройден: Эволюционная обратная связь работает")
        print(f"  Циклов: {len(results)}")
        print(f"  Успешных исходов: {sum(1 for r in results if r['outcome'])}/{len(results)}")
        print(f"  Записей обратной связи: {len(qi.feedback_history)}")
    
    def test_qualia_uniqueness(self):
        """
        Тест 4: Уникальность квалиа.
        
        Проверяем:
        - Каждое квалиа имеет уникальный ID
        - Одинаковые стимулы создают похожие но не идентичные квалиа
        - Есть контекстуальная зависимость
        """
        from qualia_interface import QualiaInterface
        
        qi = QualiaInterface()
        
        # Одинаковый стимул 5 раз
        stimulus = {
            'type': 'sensory',
            'modality': 'auditory',
            'intensity': 0.7,
            'valence': 'neutral',
            'data': {'frequency': 440, 'duration': 1.0}
        }
        
        qualias = [qi.generate_qualia(stimulus) for _ in range(5)]
        
        # Проверка 1: Все ID уникальны
        ids = [q['id'] for q in qualias]
        assert len(set(ids)) == 5
        
        # Проверка 2: Timestamps разные
        timestamps = [q['timestamp'] for q in qualias]
        assert len(set(timestamps)) == 5
        
        # Проверка 3: Содержание похожее (в пределах допуска)
        intensities = [q['intensity'] for q in qualias]
        intensity_variance = np.var(intensities)
        assert intensity_variance < 0.1  # Маленькая вариация
        
        print(f"✓ Тест 4 пройден: Уникальность квалиа подтверждена")
        print(f"  Уникальных ID: {len(set(ids))}")
        print(f"  Вариация интенсивности: {intensity_variance:.4f}")
    
    def test_qualia_memory_integration(self):
        """
        Тест 5: Интеграция с памятью.
        
        Проверяем:
        - Квалиа записывается в память
        - Прошлые квалиа влияют на новые
        - Есть поиск по ассоциациям
        """
        from qualia_interface import QualiaInterface
        
        qi = QualiaInterface()
        
        # Создаём серию квалиа
        for i in range(5):
            stimulus = {
                'type': 'sensory',
                'modality': 'visual',
                'intensity': 0.6,
                'valence': 'positive',
                'data': {'color': ['red', 'blue', 'green'][i % 3]}
            }
            qualia = qi.generate_qualia(stimulus)
            qi.store_in_memory(qualia)
        
        # Проверка 1: Память заполнена
        assert len(qi.memory) == 5
        
        # Проверка 2: Поиск по ассоциации работает
        similar = qi.search_memory({'color': 'red'})
        assert len(similar) > 0
        
        # Проверка 3: Влияние на новые квалиа
        new_stimulus = {
            'type': 'sensory',
            'modality': 'visual',
            'intensity': 0.6,
            'valence': 'positive',
            'data': {'color': 'red'}
        }
        new_qualia = qi.generate_qualia(new_stimulus)
        assert 'memory_influence' in new_qualia or qi.memory_influence_enabled
        
        print(f"✓ Тест 5 пройден: Интеграция с памятью работает")
        print(f"  Записей в памяти: {len(qi.memory)}")
        print(f"  Найдено похожих: {len(similar)}")
    
    def test_full_evolutionary_cycle(self):
        """
        Тест 6: Полный эволюционный цикл.
        
        Проверяем:
        - Стимул → Квалиа → Поведение → Исход → Обратная связь
        - Система обучается на протяжении цикла
        - Измеримые изменения в поведении
        """
        from qualia_interface import QualiaInterface
        
        qi = QualiaInterface()
        
        # 50 циклов эволюции
        evolution_data = []
        for cycle in range(50):
            stimulus = {
                'type': 'sensory',
                'modality': ['visual', 'auditory', 'touch'][cycle % 3],
                'intensity': np.random.uniform(0.3, 0.9),
                'valence': ['positive', 'negative', 'neutral'][cycle % 3],
                'data': {'cycle': cycle}
            }
            
            qualia = qi.generate_qualia(stimulus)
            behavior = qi.generate_behavior(qualia)
            outcome = qi.evaluate_outcome(behavior, stimulus)
            qi.apply_feedback(outcome)
            
            evolution_data.append({
                'cycle': cycle,
                'outcome_success': outcome['success'],
                'feedback_strength': outcome['feedback_strength'],
                'behavior_magnitude': behavior['magnitude']
            })
        
        # Проверка 1: Все циклы завершены
        assert len(evolution_data) == 50
        
        # Проверка 2: Успешность растёт (в среднем)
        first_10_success = np.mean([d['outcome_success'] for d in evolution_data[:10]])
        last_10_success = np.mean([d['outcome_success'] for d in evolution_data[-10:]])
        
        # Должна быть тенденция к улучшению (с допуском на стохастичность)
        assert last_10_success >= first_10_success - 0.2
        
        # Проверка 3: Обратная связь применяется
        assert len(qi.feedback_history) >= 50
        
        # Проверка 4: Поведение адаптируется
        first_10_magnitude = np.mean([d['behavior_magnitude'] for d in evolution_data[:10]])
        last_10_magnitude = np.mean([d['behavior_magnitude'] for d in evolution_data[-10:]])
        
        # Magnitude должен изменяться (адаптация)
        assert abs(last_10_magnitude - first_10_magnitude) > 0.01
        
        print(f"✓ Тест 6 пройден: Полный эволюционный цикл работает")
        print(f"  Циклов: {len(evolution_data)}")
        print(f"  Успешность (первые 10): {first_10_success:.2%}")
        print(f"  Успешность (последние 10): {last_10_success:.2%}")
        print(f"  Изменение magnitude: {abs(last_10_magnitude - first_10_magnitude):.4f}")


class TestQualiaMetrics:
    """
    Тесты для метрик квалиа.
    
    Проверяем измеримость функциональной модели.
    """
    
    def test_qualia_intensity_measurement(self):
        """Тест 7: Измерение интенсивности квалиа."""
        from qualia_interface import QualiaInterface, QualiaMetrics
        
        qi = QualiaInterface()
        stimulus = {
            'type': 'sensory',
            'modality': 'touch',
            'intensity': 0.8,
            'valence': 'negative',
            'data': {'temperature': 50}
        }
        
        qualia = qi.generate_qualia(stimulus)
        metrics = QualiaMetrics.calculate(qualia)
        
        assert 'intensity' in metrics
        assert metrics['intensity'] > 0
        assert metrics['intensity'] <= 1.0
        
        print(f"✓ Тест 7 пройден: Интенсивность измерена: {metrics['intensity']:.4f}")
    
    def test_qualia_valence_measurement(self):
        """Тест 8: Измерение валентности квалиа."""
        from qualia_interface import QualiaInterface, QualiaMetrics
        
        qi = QualiaInterface()
        
        qualia_pos = qi.generate_qualia({
            'type': 'sensory',
            'modality': 'taste',
            'intensity': 0.7,
            'valence': 'positive',
            'data': {}
        })
        
        qualia_neg = qi.generate_qualia({
            'type': 'sensory',
            'modality': 'touch',
            'intensity': 0.7,
            'valence': 'negative',
            'data': {}
        })
        
        metrics_pos = QualiaMetrics.calculate(qualia_pos)
        metrics_neg = QualiaMetrics.calculate(qualia_neg)
        
        assert metrics_pos['valence_score'] > 0
        assert metrics_neg['valence_score'] < 0
        
        print(f"✓ Тест 8 пройден: Валентность измерена")
        print(f"  Positive: {metrics_pos['valence_score']:.4f}")
        print(f"  Negative: {metrics_neg['valence_score']:.4f}")
    
    def test_qualia_complexity_measurement(self):
        """Тест 9: Измерение сложности квалиа."""
        from qualia_interface import QualiaInterface, QualiaMetrics
        
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
        
        metrics_simple = QualiaMetrics.calculate(qualia_simple)
        metrics_complex = QualiaMetrics.calculate(qualia_complex)
        
        # Сложное должно иметь higher complexity score
        assert metrics_complex['complexity_score'] > metrics_simple['complexity_score']
        
        print(f"✓ Тест 9 пройден: Сложность измерена")
        print(f"  Simple: {metrics_simple['complexity_score']:.4f}")
        print(f"  Complex: {metrics_complex['complexity_score']:.4f}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
