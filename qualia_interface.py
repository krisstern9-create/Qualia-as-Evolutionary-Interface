"""
Qualia-as-Evolutionary-Interface

Функциональная модель квалиа как эволюционного интерфейса.

Автор: Kris Stern
Лицензия: MIT
"""

import uuid
import time
import hashlib
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from collections import defaultdict


@dataclass
class Qualia:
    """Структура данных квалиа."""
    id: str
    timestamp: float
    intensity: float
    valence: str
    content: Dict[str, Any]
    modality: str
    memory_influence: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Behavior:
    """Структура данных поведения."""
    action: str
    direction: str
    magnitude: float
    qualia_id: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Outcome:
    """Структура данных исхода."""
    success: bool
    feedback_strength: float
    behavior_id: str
    stimulus_context: Dict[str, Any]
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class QualiaInterface:
    """Основной интерфейс для работы с квалиа."""
    
    def __init__(self, learning_rate: float = 0.1, memory_capacity: int = 1000, memory_influence_enabled: bool = True):
        """
        Инициализация интерфейса квалиа.
        
        Args:
            learning_rate: Скорость обучения (0.0 - 1.0)
            memory_capacity: Максимальный размер памяти
            memory_influence_enabled: Включено ли влияние памяти на новые квалиа
        """
        self.memory: List[Qualia] = []
        self.feedback_history: List[Outcome] = []
        self.memory_influence_enabled: bool = memory_influence_enabled
        self.learning_rate: float = learning_rate
        self.memory_capacity: int = memory_capacity
        self.adaptation_state: Dict[str, float] = defaultdict(float)
        
        self.modality_weights: Dict[str, float] = {
            'visual': 1.0, 'auditory': 1.0, 'touch': 1.0,
            'taste': 1.0, 'olfactory': 1.0, 'multimodal': 1.5,
            'sensory': 1.0
        }
        
        self.valence_weights: Dict[str, float] = {
            'positive': 1.0, 'negative': 1.2, 'neutral': 0.8
        }
    
    def generate_qualia(self, stimulus: Dict[str, Any]) -> Qualia:
        """Генерация квалиа из стимула."""
        qualia_id = self._generate_qualia_id(stimulus)
        timestamp = time.time()
        
        modality = stimulus.get('modality', 'sensory')
        modality_weight = self.modality_weights.get(modality, 1.0)
        base_intensity = stimulus.get('intensity', 0.5)
        intensity = np.clip(base_intensity * modality_weight, 0.0, 1.0)
        
        valence = stimulus.get('valence', 'neutral')
        
        memory_influence = None
        if self.memory_influence_enabled and len(self.memory) > 0:
            memory_influence = self._compute_memory_influence(stimulus)
            if memory_influence and 'intensity_modifier' in memory_influence:
                intensity = np.clip(intensity * memory_influence['intensity_modifier'], 0.0, 1.0)
        
        content = self._process_stimulus_content(stimulus)
        
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
                'processing_cycles': len(self.feedback_history)
            }
        )
        
        return qualia
    
    def generate_behavior(self, qualia: Qualia) -> Behavior:
        """Генерация поведения из квалиа."""
        timestamp = time.time()
        
        if qualia.valence == 'positive':
            direction = 'approach'
        elif qualia.valence == 'negative':
            direction = 'avoid'
        else:
            direction = 'neutral'
        
        base_magnitude = qualia.intensity
        adaptation_factor = self.adaptation_state.get(qualia.modality, 1.0)
        magnitude = np.clip(base_magnitude * adaptation_factor, 0.0, 1.0)
        
        noise = np.random.normal(0, 0.05)
        magnitude = np.clip(magnitude + noise, 0.0, 1.0)
        
        action = self._determine_action(qualia)
        
        behavior = Behavior(
            action=action,
            direction=direction,
            magnitude=magnitude,
            qualia_id=qualia.id,
            timestamp=timestamp,
            metadata={
                'valence': qualia.valence,
                'modality': qualia.modality
            }
        )
        
        return behavior
    
    def evaluate_outcome(self, behavior: Behavior, stimulus: Dict[str, Any]) -> Outcome:
        """Оценка исхода поведения."""
        timestamp = time.time()
        
        stimulus_valence = stimulus.get('valence', 'neutral')
        
        success_mapping = {
            ('positive', 'approach'): True,
            ('negative', 'avoid'): True,
            ('neutral', 'neutral'): True,
            ('positive', 'avoid'): False,
            ('negative', 'approach'): False,
        }
        
        key = (stimulus_valence, behavior.direction)
        base_success = success_mapping.get(key, True)
        
        noise = np.random.normal(0, 0.1)
        success = base_success if noise > -0.1 else not base_success
        
        feedback_strength = behavior.magnitude * self.learning_rate
        if success:
            feedback_strength *= 1.2
        
        outcome = Outcome(
            success=success,
            feedback_strength=feedback_strength,
            behavior_id=behavior.qualia_id,
            stimulus_context={
                'valence': stimulus_valence,
                'modality': stimulus.get('modality', 'sensory')
            },
            timestamp=timestamp,
            metadata={'behavior_magnitude': behavior.magnitude}
        )
        
        return outcome
    
    def apply_feedback(self, outcome: Outcome) -> None:
        """Применение обратной связи."""
        self.feedback_history.append(outcome)
        
        modality = outcome.stimulus_context.get('modality', 'sensory')
        
        if outcome.success:
            self.adaptation_state[modality] += outcome.feedback_strength
        else:
            self.adaptation_state[modality] -= outcome.feedback_strength * 0.5
        
        self.adaptation_state[modality] = np.clip(
            self.adaptation_state[modality], 0.5, 2.0
        )
    
    def store_in_memory(self, qualia: Qualia) -> None:
        """Сохранение квалиа в памяти."""
        self.memory.append(qualia)
        
        if len(self.memory) > self.memory_capacity:
            self.memory = self.memory[-self.memory_capacity:]
    
    def search_memory(self, query: Dict[str, Any]) -> List[Qualia]:
        """Поиск похожих квалиа в памяти."""
        if not self.memory:
            return []
        
        results = []
        for qualia in self.memory:
            if self._match_content(qualia.content, query):
                results.append(qualia)
        
        return results
    
    def _generate_qualia_id(self, stimulus: Dict[str, Any]) -> str:
        """Генерация уникального ID."""
        unique_data = f"{time.time()}-{uuid.uuid4()}-{str(stimulus)}"
        return hashlib.sha256(unique_data.encode()).hexdigest()
    
    def _compute_memory_influence(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """Вычисление влияния памяти."""
        similar_qualias = self.search_memory(stimulus.get('data', {}))
        
        if not similar_qualias:
            return {'intensity_modifier': 1.0, 'valence_bias': 0.0}
        
        avg_intensity = np.mean([q.intensity for q in similar_qualias[:5]])
        intensity_modifier = 1.0 + (avg_intensity - 0.5) * 0.2
        
        positive_count = sum(1 for q in similar_qualias if q.valence == 'positive')
        valence_bias = (positive_count / len(similar_qualias)) - 0.5
        
        return {
            'intensity_modifier': float(np.clip(intensity_modifier, 0.8, 1.2)),
            'valence_bias': float(valence_bias),
            'similar_count': len(similar_qualias)
        }
    
    def _process_stimulus_content(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка содержания стимула."""
        content = {
            'modality': stimulus.get('modality', 'sensory'),
            'raw_data': stimulus.get('data', {}),
            'processed_features': []
        }
        
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
        """Определение действия."""
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
        """Проверка соответствия содержания."""
        if not query:
            return False
        
        for key, value in query.items():
            if key in content.get('raw_data', {}):
                if content['raw_data'][key] == value:
                    return True
            
            for feature in content.get('processed_features', []):
                if feature.get('feature') == key and feature.get('value') == value:
                    return True
        
        return False
