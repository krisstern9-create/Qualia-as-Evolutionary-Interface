"""
Qualia-as-Evolutionary-Interface

Функциональная модель квалиа как эволюционного интерфейса.
Квалиа — не метафизическая сущность, а вычислительный процесс,
который преобразует стимулы в поведение через субъективный опыт
с эволюционной обратной связью.

Автор: Kris Stern
Лицензия: MIT
"""

import uuid
import time
import hashlib
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Qualia:
    """
    Структура данных квалиа.
    
    Квалиа — это измеримый вычислительный паттерн,
    возникающий при обработке стимула.
    """
    id: str
    timestamp: float
    intensity: float
    valence: str  # 'positive', 'negative', 'neutral'
    content: Dict[str, Any]
    modality: str
    memory_influence: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Qualia':
        return cls(**data)


@dataclass
class Behavior:
    """
    Структура данных поведения.
    
    Поведение — это выходной сигнал системы,
    сгенерированный на основе квалиа.
    """
    action: str
    direction: str  # 'approach', 'avoid', 'neutral'
    magnitude: float
    qualia_id: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Outcome:
    """
    Структура данных исхода.
    
    Исход — это результат поведения в среде,
    используемый для эволюционной обратной связи.
    """
    success: bool
    feedback_strength: float
    behavior_id: str
    stimulus_context: Dict[str, Any]
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =============================================================================
# QUALIA INTERFACE
# =============================================================================

class QualiaInterface:
    """
    Основной интерфейс для работы с квалиа.
    
    Реализует полный цикл:
    Стимул → Квалиа → Поведение → Исход → Обратная связь → Адаптация
    
    Атрибуты:
        memory: Список всех сохранённых квалиа
        feedback_history: История всей обратной связи
        memory_influence_enabled: Включено ли влияние памяти на новые квалиа
        learning_rate: Скорость адаптации системы
    """
    
    def __init__(self, learning_rate: float = 0.1, memory_capacity: int = 1000):
        """
        Инициализация интерфейса квалиа.
        
        Args:
            learning_rate: Скорость обучения (0.0 - 1.0)
            memory_capacity: Максимальный размер памяти
        """
        self.memory: List[Qualia] = []
        self.feedback_history: List[Outcome] = []
        self.memory_influence_enabled: bool = True
        self.learning_rate: float = learning_rate
        self.memory_capacity: int = memory_capacity
        self.adaptation_state: Dict[str, float] = defaultdict(float)
        
        # Веса для различных модальностей
        self.modality_weights: Dict[str, float] = {
            'visual': 1.0,
            'auditory': 1.0,
            'touch': 1.0,
            'taste': 1.0,
            'olfactory': 1.0,
            'multimodal': 1.5,
            'sensory': 1.0
        }
        
        # Веса для валентностей
        self.valence_weights: Dict[str, float] = {
            'positive': 1.0,
            'negative': 1.2,  # Отрицательные стимулы имеют больший вес (выживание)
            'neutral': 0.8
        }
    
    def generate_qualia(self, stimulus: Dict[str, Any]) -> Qualia:
        """
        Генерация квалиа из стимула.
        
        Args:
            stimulus: Входной стимул со структурой:
                - type: тип стимула ('sensory', 'cognitive', etc.)
                - modality: модальность ('visual', 'auditory', etc.)
                - intensity: интенсивность (0.0 - 1.0)
                - valence: валентность ('positive', 'negative', 'neutral')
                - data: дополнительные данные стимула
        
        Returns:
            Qualia: Сгенерированное квалиа с уникальным ID и метаданными
        """
        # Генерация уникального ID
        qualia_id = self._generate_qualia_id(stimulus)
        timestamp = time.time()
        
        # Расчёт интенсивности с учётом модальности
        modality = stimulus.get('modality', 'sensory')
        modality_weight = self.modality_weights.get(modality, 1.0)
        base_intensity = stimulus.get('intensity', 0.5)
        intensity = np.clip(base_intensity * modality_weight, 0.0, 1.0)
        
        # Валентность
        valence = stimulus.get('valence', 'neutral')
        valence_weight = self.valence_weights.get(valence, 1.0)
        
        # Влияние памяти (если включено)
        memory_influence = None
        if self.memory_influence_enabled and len(self.memory) > 0:
            memory_influence = self._compute_memory_influence(stimulus)
            # Коррекция интенсивности на основе памяти
            if memory_influence and 'intensity_modifier' in memory_influence:
                intensity = np.clip(intensity * memory_influence['intensity_modifier'], 0.0, 1.0)
        
        # Формирование содержания квалиа
        content = self._process_stimulus_content(stimulus)
        
        # Создание квалиа
        qualia = Qualia(
            id=qualia_id,
            timestamp=timestamp,
            intensity=intensity,
            valence=valence,
            content=content,
            modality=modality,
            memory_influence=memory_influence,
            metadata={
                'stimulus_hash': hashlib.sha256(str(stimulus).encode()).hexdigest()[:16],
                'processing_cycles': len(self.feedback_history),
                'adaptation_state': dict(self.adaptation_state)
            }
        )
        
        return qualia
    
    def generate_behavior(self, qualia: Qualia) -> Behavior:
        """
        Генерация поведения из квалиа.
        
        Args:
            qualia: Входное квалиа
        
        Returns:
            Behavior: Сгенерированное поведение с направлением и магнитудой
        """
        timestamp = time.time()
        
        # Определение направления на основе валентности
        if qualia.valence == 'positive':
            direction = 'approach'
        elif qualia.valence == 'negative':
            direction = 'avoid'
        else:
            direction = 'neutral'
        
        # Расчёт магнитуды на основе интенсивности
        base_magnitude = qualia.intensity
        
        # Коррекция на основе адаптации
        adaptation_factor = self.adaptation_state.get(qualia.modality, 1.0)
        magnitude = np.clip(base_magnitude * adaptation_factor, 0.0, 1.0)
        
        # Добавление стохастичности (вариативность поведения)
        noise = np.random.normal(0, 0.05)
        magnitude = np.clip(magnitude + noise, 0.0, 1.0)
        
        # Определение действия на основе содержания
        action = self._determine_action(qualia)
        
        behavior = Behavior(
            action=action,
            direction=direction,
            magnitude=magnitude,
            qualia_id=qualia.id,
            timestamp=timestamp,
            metadata={
                'valence': qualia.valence,
                'modality': qualia.modality,
                'intensity': qualia.intensity
            }
        )
        
        return behavior
    
    def evaluate_outcome(self, behavior: Behavior, stimulus: Dict[str, Any]) -> Outcome:
        """
        Оценка исхода поведения.
        
        Args:
            behavior: Выполненное поведение
            stimulus: Исходный стимул
        
        Returns:
            Outcome: Результат с успешностью и силой обратной связи
        """
        timestamp = time.time()
        
        # Оценка успешности на основе соответствия валентности и направления
        stimulus_valence = stimulus.get('valence', 'neutral')
        
        # Положительная валентность + approach = успех
        # Отрицательная валентность + avoid = успех
        success_mapping = {
            ('positive', 'approach'): True,
            ('negative', 'avoid'): True,
            ('neutral', 'neutral'): True,
            ('positive', 'avoid'): False,
            ('negative', 'approach'): False,
        }
        
        key = (stimulus_valence, behavior.direction)
        base_success = success_mapping.get(key, True)
        
        # Добавление стохастичности (среда не детерминирована)
        noise = np.random.normal(0, 0.1)
        success = base_success if noise > -0.1 else not base_success
        
        # Расчёт силы обратной связи
        feedback_strength = behavior.magnitude * self.learning_rate
        if success:
            feedback_strength *= 1.2  # Успех усиливает обратную связь
        
        outcome = Outcome(
            success=success,
            feedback_strength=feedback_strength,
            behavior_id=behavior.qualia_id,
            stimulus_context={
                'valence': stimulus_valence,
                'modality': stimulus.get('modality', 'sensory'),
                'intensity': stimulus.get('intensity', 0.5)
            },
            timestamp=timestamp,
            metadata={
                'behavior_magnitude': behavior.magnitude,
                'behavior_direction': behavior.direction
            }
        )
        
        return outcome
    
    def apply_feedback(self, outcome: Outcome) -> None:
        """
        Применение обратной связи для адаптации системы.
        
        Args:
            outcome: Исход для применения обратной связи
        """
        # Запись в историю
        self.feedback_history.append(outcome)
        
        # Адаптация весов на основе исхода
        modality = outcome.stimulus_context.get('modality', 'sensory')
        
        if outcome.success:
            # Успех усиливает текущую стратегию
            self.adaptation_state[modality] += outcome.feedback_strength
        else:
            # Неудача ослабляет текущую стратегию
            self.adaptation_state[modality] -= outcome.feedback_strength * 0.5
        
        # Ограничение диапазона адаптации
        self.adaptation_state[modality] = np.clip(
            self.adaptation_state[modality], 0.5, 2.0
        )
    
    def store_in_memory(self, qualia: Qualia) -> None:
        """
        Сохранение квалиа в памяти.
        
        Args:
            qualia: Квалиа для сохранения
        """
        self.memory.append(qualia)
        
        # Ограничение размера памяти
        if len(self.memory) > self.memory_capacity:
            self.memory = self.memory[-self.memory_capacity:]
    
    def search_memory(self, query: Dict[str, Any]) -> List[Qualia]:
        """
        Поиск похожих квалиа в памяти.
        
        Args:
            query: Критерии поиска (например, {'color': 'red'})
        
        Returns:
            List[Qualia]: Список похожих квалиа
        """
        if not self.memory:
            return []
        
        results = []
        for qualia in self.memory:
            # Проверка содержания на соответствие запросу
            match = self._match_content(qualia.content, query)
            if match:
                results.append(qualia)
        
        return results
    
    def _generate_qualia_id(self, stimulus: Dict[str, Any]) -> str:
        """Генерация уникального ID для квалиа."""
        unique_data = f"{time.time()}-{uuid.uuid4()}-{str(stimulus)}"
        return hashlib.sha256(unique_data.encode()).hexdigest()
    
    def _compute_memory_influence(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """
        Вычисление влияния памяти на новое квалиа.
        
        Ищет похожие стимулы в памяти и возвращает модификаторы.
        """
        similar_qualias = self.search_memory(stimulus.get('data', {}))
        
        if not similar_qualias:
            return {'intensity_modifier': 1.0, 'valence_bias': 0.0}
        
        # Усреднение интенсивности похожих квалиа
        avg_intensity = np.mean([q.intensity for q in similar_qualias[:5]])
        intensity_modifier = 1.0 + (avg_intensity - 0.5) * 0.2
        
        # bias валентности
        positive_count = sum(1 for q in similar_qualias if q.valence == 'positive')
        valence_bias = (positive_count / len(similar_qualias)) - 0.5
        
        return {
            'intensity_modifier': float(np.clip(intensity_modifier, 0.8, 1.2)),
            'valence_bias': float(valence_bias),
            'similar_count': len(similar_qualias)
        }
    
    def _process_stimulus_content(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка содержания стимула для квалиа."""
        content = {
            'modality': stimulus.get('modality', 'sensory'),
            'raw_data': stimulus.get('data', {}),
            'processed_features': []
        }
        
        # Извлечение признаков из данных стимула
        data = stimulus.get('data', {})
        for key, value in data.items():
            if isinstance(value, (int, float)):
                content['processed_features'].append({
                    'feature': key,
                    'value': float(value),
                    'normalized': float(np.clip(value, 0, 1))
                })
            elif isinstance(value, str):
                content['processed_features'].append({
                    'feature': key,
                    'value': value,
                    'hash': hashlib.md5(value.encode()).hexdigest()[:8]
                })
        
        return content
    
    def _determine_action(self, qualia: Qualia) -> str:
        """Определение действия на основе квалиа."""
        action_mapping = {
            ('visual', 'positive'): 'observe',
            ('visual', 'negative'): 'look_away',
            ('auditory', 'positive'): 'listen',
            ('auditory', 'negative'): 'block_sound',
            ('touch', 'positive'): 'touch_more',
            ('touch', 'negative'): 'withdraw',
            ('taste', 'positive'): 'consume',
            ('taste', 'negative'): 'reject',
            ('multimodal', 'positive'): 'engage',
            ('multimodal', 'negative'): 'disengage',
        }
        
        key = (qualia.modality, qualia.valence)
        return action_mapping.get(key, 'respond')
    
    def _match_content(self, content: Dict[str, Any], query: Dict[str, Any]) -> bool:
        """Проверка соответствия содержания запросу."""
        if not query:
            return False
        
        for key, value in query.items():
            # Поиск в raw_data
            if key in content.get('raw_data', {}):
                if content['raw_data'][key] == value:
                    return True
            
            # Поиск в processed_features
            for feature in content.get('processed_features', []):
                if feature.get('feature') == key and feature.get('value') == value:
                    return True
        
        return False


# =============================================================================
# QUALIA METRICS
# =============================================================================

class QualiaMetrics:
    """
    Метрики для измерения квалиа.
    
    Предоставляет количественные измерения:
    - Интенсивность
    - Валентность
    - Сложность
    - Уникальность
    """
    
    @staticmethod
    def calculate(qualia: Qualia) -> Dict[str, float]:
        """
        Расчёт всех метрик для квалиа.
        
        Args:
            qualia: Квалиа для измерения
        
        Returns:
            Dict[str, float]: Словарь с метриками
        """
        return {
            'intensity': qualia.intensity,
            'valence_score': QualiaMetrics._calculate_valence_score(qualia),
            'complexity_score': QualiaMetrics._calculate_complexity_score(qualia),
            'uniqueness_score': QualiaMetrics._calculate_uniqueness_score(qualia),
            'memory_influence_score': QualiaMetrics._calculate_memory_influence_score(qualia)
        }
    
    @staticmethod
    def _calculate_valence_score(qualia: Qualia) -> float:
        """
        Расчёт scores валентности (-1.0 до 1.0).
        
        positive → положительный score
        negative → отрицательный score
        neutral → около 0
        """
        valence_mapping = {
            'positive': 1.0,
            'negative': -1.0,
            'neutral': 0.0
        }
        
        base_score = valence_mapping.get(qualia.valence, 0.0)
        
        # Коррекция на основе интенсивности
        score = base_score * qualia.intensity
        
        return float(np.clip(score, -1.0, 1.0))
    
    @staticmethod
    def _calculate_complexity_score(qualia: Qualia) -> float:
        """
        Расчёт сложности квалиа (0.0 до 1.0).
        
        Учитывает:
        - Количество признаков в содержании
        - Разнообразие модальностей
        - Глубину вложенности данных
        """
        content = qualia.content
        
        # Количество признаков
        feature_count = len(content.get('processed_features', []))
        feature_score = min(feature_count / 10.0, 1.0)
        
        # Разнообразие данных
        raw_data = content.get('raw_data', {})
        diversity_score = min(len(raw_data) / 5.0, 1.0)
        
        # Мультимодальность
        modality_bonus = 0.2 if qualia.modality == 'multimodal' else 0.0
        
        # Итоговая сложность
        complexity = (feature_score * 0.4 + diversity_score * 0.4 + modality_bonus * 0.2)
        
        return float(np.clip(complexity, 0.0, 1.0))
    
    @staticmethod
    def _calculate_uniqueness_score(qualia: Qualia) -> float:
        """
        Расчёт уникальности квалиа (0.0 до 1.0).
        
        Основано на:
        - Уникальности ID (всегда уникален)
        - Временной метке
        - Комбинации признаков
        """
        # ID уже уникален, но добавляем вариацию на основе содержания
        content_hash = hashlib.sha256(str(qualia.content).encode()).hexdigest()
        hash_value = int(content_hash[:8], 16) / 0xFFFFFFFF
        
        # Временная уникальность
        time_component = (qualia.timestamp % 1.0)
        
        uniqueness = (hash_value * 0.7 + time_component * 0.3)
        
        return float(np.clip(uniqueness, 0.0, 1.0))
    
    @staticmethod
    def _calculate_memory_influence_score(qualia: Qualia) -> float:
        """
        Расчёт влияния памяти на квалиа (0.0 до 1.0).
        """
        if qualia.memory_influence is None:
            return 0.0
        
        influence = qualia.memory_influence
        
        # Количество похожих квалиа
        similar_count = influence.get('similar_count', 0)
        count_score = min(similar_count / 10.0, 1.0)
        
        # Сила модификатора интенсивности
        intensity_mod = influence.get('intensity_modifier', 1.0)
        mod_score = abs(intensity_mod - 1.0) * 2  # Нормализация
        
        influence_score = (count_score * 0.6 + mod_score * 0.4)
        
        return float(np.clip(influence_score, 0.0, 1.0))
    
    @staticmethod
    def compare(qualia1: Qualia, qualia2: Qualia) -> Dict[str, float]:
        """
        Сравнение двух квалиа.
        
        Args:
            qualia1: Первое квалиа
            qualia2: Второе квалиа
        
        Returns:
            Dict[str, float]: Метрики сравнения
        """
        metrics1 = QualiaMetrics.calculate(qualia1)
        metrics2 = QualiaMetrics.calculate(qualia2)
        
        return {
            'intensity_diff': abs(metrics1['intensity'] - metrics2['intensity']),
            'valence_diff': abs(metrics1['valence_score'] - metrics2['valence_score']),
            'complexity_diff': abs(metrics1['complexity_score'] - metrics2['complexity_score']),
            'similarity_score': 1.0 - (
                abs(metrics1['intensity'] - metrics2['intensity']) * 0.4 +
                abs(metrics1['valence_score'] - metrics2['valence_score']) * 0.4 +
                abs(metrics1['complexity_score'] - metrics2['complexity_score']) * 0.2
            )
        }
