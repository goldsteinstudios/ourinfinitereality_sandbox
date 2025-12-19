"""
Translation Engine: Multi-layer structural decoder for Dao De Jing
Reveals the operational mechanics encoded in radical composition
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import json

from radical_dictionary import get_radicals, get_radical_category, RADICAL_CATEGORIES


@dataclass
class RadicalOperation:
    """Represents what a radical DOES in context"""
    radical: str
    category: str
    operation: str  # What transformation/action it marks
    position: str   # Where it sits in the character (left, right, top, bottom, surround)


@dataclass
class CharacterStructure:
    """Complete structural analysis of a character"""
    char: str
    radicals: List[RadicalOperation]
    composition: str  # How radicals combine: "left+right", "top+bottom", "surround+inside"
    structural_formula: str  # What it builds: "Process(continuous, primary)"
    slot_grammar: List[str]  # Grammatical roles: ["operation", "context"]
    topological_type: str  # P, O, G, frame, perception, etc.


@dataclass
class TranslationLayer:
    """One layer of the multi-layer translation"""
    level: str  # "surface", "operational", "structural", "pattern"
    content: str
    annotations: Dict[str, str]


# Character Operation Database
# This is the "engineering manual" - what each character actually DOES
CHARACTER_OPERATIONS = {
    # === CHAPTER 1 CHARACTERS ===

    '道': {
        'radicals': [
            {'radical': '辶', 'category': 'motion', 'operation': 'continuous_motion_through_space', 'position': 'surround'},
            {'radical': '首', 'category': 'entity', 'operation': 'primary/head/governing', 'position': 'inside'}
        ],
        'composition': 'motion_surrounds_primary',
        'formula': 'Process(continuous=True, governing=True)',
        'slot_grammar': ['operation', 'primacy'],
        'topo_type': 'O',  # Origin/ongoing process
        'notes': 'The Way - primary continuous process that generates without forcing'
    },

    '可': {
        'radicals': [
            {'radical': '口', 'category': 'boundary', 'operation': 'frame/boundary', 'position': 'left'},
            {'radical': '丁', 'category': 'structure', 'operation': 'nail/pin/fix', 'position': 'right'}
        ],
        'composition': 'boundary+fixation',
        'formula': 'Fixable(to_frame=True)',
        'slot_grammar': ['ability', 'constraint'],
        'topo_type': 'frame',
        'notes': 'Can be pinned/named - ability to constrain to a boundary'
    },

    '名': {
        'radicals': [
            {'radical': '口', 'category': 'boundary', 'operation': 'boundary/distinction', 'position': 'top'},
            {'radical': '夕', 'category': 'temporal', 'operation': 'night/hidden', 'position': 'bottom'}
        ],
        'composition': 'boundary+temporal',
        'formula': 'Name(explicit_distinction=True)',
        'slot_grammar': ['designation', 'boundary'],
        'topo_type': 'frame',
        'notes': 'Naming - creating explicit boundary/distinction'
    },

    '常': {
        'radicals': [
            {'radical': '巾', 'category': 'cloth', 'operation': 'fabric/pattern', 'position': 'bottom'},
            {'radical': '尚', 'category': 'magnitude', 'operation': 'value/esteem', 'position': 'top'}
        ],
        'composition': 'value+pattern',
        'formula': 'Constant(pattern=True, frame_independent=True)',
        'slot_grammar': ['state', 'persistence'],
        'topo_type': 'O',
        'notes': 'Constant/eternal - frame-independent pattern fabric'
    },

    '無': {
        'radicals': [
            {'radical': '火', 'category': 'transformation', 'operation': 'transformation_energy', 'position': 'core'}
        ],
        'composition': 'fire_transformation_in_absence_mode',
        'formula': 'Transform(mode=absence, active=True)',
        'slot_grammar': ['operation', 'mode'],
        'topo_type': 'O',
        'notes': 'Nothing/without - transformation through absence, NOT mere void'
    },

    '為': {
        'radicals': [
            {'radical': '火', 'category': 'transformation', 'operation': 'transformation_energy', 'position': 'core'}
        ],
        'composition': 'fire_transformation_in_action_mode',
        'formula': 'Transform(mode=action, forcing=True)',
        'slot_grammar': ['operation', 'mode'],
        'topo_type': 'G',
        'notes': 'Do/act/make - transformation through action, paired with 無'
    },

    '有': {
        'radicals': [
            {'radical': '月', 'category': 'temporal', 'operation': 'cycle/presence', 'position': 'core'}
        ],
        'composition': 'temporal_presence',
        'formula': 'Exist(manifest=True, bounded=True)',
        'slot_grammar': ['state', 'presence'],
        'topo_type': 'P',
        'notes': 'Have/exist - bounded manifest presence'
    },

    '天': {
        'radicals': [
            {'radical': '大', 'category': 'magnitude', 'operation': 'great/expansive', 'position': 'base'},
            {'radical': '一', 'category': 'structure', 'operation': 'horizontal/covering', 'position': 'top'}
        ],
        'composition': 'great+covering',
        'formula': 'Heaven(scale=maximal, boundary=upper)',
        'slot_grammar': ['domain', 'upper_bound'],
        'topo_type': 'frame',
        'notes': 'Heaven/sky - maximal covering boundary'
    },

    '下': {
        'radicals': [
            {'radical': '一', 'category': 'structure', 'operation': 'horizontal/base', 'position': 'top'},
            {'radical': '丶', 'category': 'structure', 'operation': 'point/marker', 'position': 'below'}
        ],
        'composition': 'base+below_marker',
        'formula': 'Below(reference=horizon)',
        'slot_grammar': ['position', 'lower_bound'],
        'topo_type': 'frame',
        'notes': 'Below/under - position beneath reference line'
    },

    '玄': {
        'radicals': [
            {'radical': '玄', 'category': 'other', 'operation': 'dark/mysterious/subtle', 'position': 'whole'}
        ],
        'composition': 'dark_subtle_thread',
        'formula': 'Mysterious(paradoxical=True, origin=True)',
        'slot_grammar': ['state', 'quality'],
        'topo_type': 'O',
        'notes': 'Mysterious/dark - paradoxical origin point, pre-distinction'
    },

    '之': {
        'radicals': [
            {'radical': '丶', 'category': 'structure', 'operation': 'point/marker', 'position': 'top'},
            {'radical': '一', 'category': 'structure', 'operation': 'connection', 'position': 'through'}
        ],
        'composition': 'point+connection',
        'formula': 'Of(connection=True, possessive=True)',
        'slot_grammar': ['relation', 'connection'],
        'topo_type': 'connection',
        'notes': 'Of/possessive - marks connection/relationship'
    },

    '萬': {
        'radicals': [
            {'radical': '艸', 'category': 'other', 'operation': 'grass/growth', 'position': 'top'}
        ],
        'composition': 'myriad_growth',
        'formula': 'Myriad(countless=True, generative=True)',
        'slot_grammar': ['quantity', 'multiplicity'],
        'topo_type': 'G',
        'notes': 'Ten thousand/myriad - countless manifestations'
    },

    '物': {
        'radicals': [
            {'radical': '牛', 'category': 'entity', 'operation': 'being/creature', 'position': 'left'},
            {'radical': '勿', 'category': 'action', 'operation': 'not/cutting', 'position': 'right'}
        ],
        'composition': 'being+distinction',
        'formula': 'Thing(manifest=True, distinct=True)',
        'slot_grammar': ['entity', 'manifestation'],
        'topo_type': 'P',
        'notes': 'Thing/being - distinct manifest entity'
    },

    '始': {
        'radicals': [
            {'radical': '女', 'category': 'entity', 'operation': 'feminine/receptive', 'position': 'left'},
            {'radical': '台', 'category': 'structure', 'operation': 'platform/beginning', 'position': 'right'}
        ],
        'composition': 'receptive+origin',
        'formula': 'Begin(from_void=True, receptive=True)',
        'slot_grammar': ['temporal', 'origin'],
        'topo_type': 'O',
        'notes': 'Beginning - origin through receptivity'
    },

    '母': {
        'radicals': [
            {'radical': '女', 'category': 'entity', 'operation': 'feminine/receptive', 'position': 'base'}
        ],
        'composition': 'feminine_generative',
        'formula': 'Mother(generative=True, source=True)',
        'slot_grammar': ['source', 'generator'],
        'topo_type': 'O',
        'notes': 'Mother - generative source'
    },

    # === ADDITIONAL CHAPTER 1 CHARACTERS ===

    '非': {
        'radicals': [
            {'radical': '非', 'category': 'connection', 'operation': 'negation/wings_diverging', 'position': 'whole'}
        ],
        'composition': 'wings_flying_apart',
        'formula': 'Not(negation=True, divergence=True)',
        'slot_grammar': ['negation', 'contrast'],
        'topo_type': 'connection',
        'notes': 'Not/non - negation, wings diverging (flying apart from)'
    },

    '地': {
        'radicals': [
            {'radical': '土', 'category': 'structure', 'operation': 'earth/ground', 'position': 'left'}
        ],
        'composition': 'earth_foundation',
        'formula': 'Earth(grounded=True, lower_realm=True)',
        'slot_grammar': ['domain', 'foundation'],
        'topo_type': 'P',
        'notes': 'Earth/ground - lower bounded domain, complementary to heaven'
    },

    '故': {
        'radicals': [
            {'radical': '古', 'category': 'temporal', 'operation': 'ancient/old', 'position': 'left'},
            {'radical': '攴', 'category': 'action', 'operation': 'tap/strike', 'position': 'right'}
        ],
        'composition': 'ancient+action',
        'formula': 'Therefore(causal=True, reason=True)',
        'slot_grammar': ['conjunction', 'causation'],
        'topo_type': 'connection',
        'notes': 'Therefore/thus - causal connector, because of ancient pattern'
    },

    '欲': {
        'radicals': [
            {'radical': '谷', 'category': 'boundary', 'operation': 'valley/hollow', 'position': 'left'},
            {'radical': '欠', 'category': 'entity', 'operation': 'lack/yawn', 'position': 'right'}
        ],
        'composition': 'valley+lack',
        'formula': 'Desire(oriented=True, vector=True)',
        'slot_grammar': ['intention', 'direction'],
        'topo_type': 'G',
        'notes': 'Desire/want - directional vector/orientation toward'
    },

    '以': {
        'radicals': [
            {'radical': '人', 'category': 'agent', 'operation': 'person', 'position': 'implied'}
        ],
        'composition': 'person_using',
        'formula': 'By_means_of(instrument=True)',
        'slot_grammar': ['preposition', 'instrument'],
        'topo_type': 'connection',
        'notes': 'By means of/in order to - instrumental connector'
    },

    '觀': {
        'radicals': [
            {'radical': '見', 'category': 'perception', 'operation': 'see/perceive', 'position': 'right'},
            {'radical': '雚', 'category': 'entity', 'operation': 'bird/observe', 'position': 'left'}
        ],
        'composition': 'bird+seeing',
        'formula': 'Observe(comprehensive=True, overview=True)',
        'slot_grammar': ['perception', 'observation'],
        'topo_type': 'perception',
        'notes': 'Observe/contemplate - comprehensive seeing (bird\'s eye view)'
    },

    '其': {
        'radicals': [
            {'radical': '八', 'category': 'structure', 'operation': 'divide/diverge', 'position': 'top'}
        ],
        'composition': 'dividing_structure',
        'formula': 'Its(reference=True, demonstrative=True)',
        'slot_grammar': ['pronoun', 'reference'],
        'topo_type': 'connection',
        'notes': 'Its/that - demonstrative pronoun, points to referent'
    },

    '妙': {
        'radicals': [
            {'radical': '女', 'category': 'entity', 'operation': 'feminine/receptive', 'position': 'left'},
            {'radical': '少', 'category': 'magnitude', 'operation': 'few/small/subtle', 'position': 'right'}
        ],
        'composition': 'feminine+subtle',
        'formula': 'Subtle(fine=True, mystery=True)',
        'slot_grammar': ['quality', 'subtlety'],
        'topo_type': 'O',
        'notes': 'Subtle/mysterious/wondrous - fine distinctions, feminine subtlety'
    },

    '徼': {
        'radicals': [
            {'radical': '彳', 'category': 'motion', 'operation': 'step/walk', 'position': 'left'},
            {'radical': '敫', 'category': 'action', 'operation': 'seek/patrol', 'position': 'right'}
        ],
        'composition': 'walking+seeking',
        'formula': 'Boundary_patrol(manifest=True, perimeter=True)',
        'slot_grammar': ['boundary', 'manifestation'],
        'topo_type': 'P',
        'notes': 'Manifest boundaries/limits - patrolling the perimeter'
    },

    '此': {
        'radicals': [
            {'radical': '止', 'category': 'motion', 'operation': 'stop/foot', 'position': 'bottom'},
            {'radical': '匕', 'category': 'structure', 'operation': 'spoon/ladle', 'position': 'top'}
        ],
        'composition': 'stop+indicate',
        'formula': 'This(proximal=True, demonstrative=True)',
        'slot_grammar': ['pronoun', 'demonstrative'],
        'topo_type': 'connection',
        'notes': 'This - proximal demonstrative, stops and points here'
    },

    '兩': {
        'radicals': [
            {'radical': '一', 'category': 'structure', 'operation': 'horizontal/line', 'position': 'top'},
            {'radical': '一', 'category': 'structure', 'operation': 'horizontal/line', 'position': 'bottom'}
        ],
        'composition': 'two_parallel_lines',
        'formula': 'Two(duality=True, pair=True)',
        'slot_grammar': ['number', 'duality'],
        'topo_type': 'frame',
        'notes': 'Two/both - duality, paired opposites'
    },

    '者': {
        'radicals': [
            {'radical': '老', 'category': 'entity', 'operation': 'old/elder', 'position': 'top'}
        ],
        'composition': 'elder_marker',
        'formula': 'One_who(nominalizer=True)',
        'slot_grammar': ['nominalizer', 'entity_marker'],
        'topo_type': 'frame',
        'notes': 'One who/that which - nominalizer, creates entity from process'
    },

    '同': {
        'radicals': [
            {'radical': '口', 'category': 'boundary', 'operation': 'mouth/opening', 'position': 'outer'},
            {'radical': '一', 'category': 'structure', 'operation': 'unity/together', 'position': 'inside'}
        ],
        'composition': 'enclosed_unity',
        'formula': 'Same(identity=True, unified=True)',
        'slot_grammar': ['identity', 'sameness'],
        'topo_type': 'connection',
        'notes': 'Same/together - shared identity within boundary'
    },

    '出': {
        'radicals': [
            {'radical': '凵', 'category': 'boundary', 'operation': 'container/receptacle', 'position': 'outer'},
            {'radical': '山', 'category': 'structure', 'operation': 'mountain/peaks', 'position': 'emerging'}
        ],
        'composition': 'emergence_from_container',
        'formula': 'Emerge(from_within=True, outward=True)',
        'slot_grammar': ['motion', 'emergence'],
        'topo_type': 'G',
        'notes': 'Come out/emerge - emergence from container/source'
    },

    '而': {
        'radicals': [
            {'radical': '而', 'category': 'connection', 'operation': 'and_yet/beard', 'position': 'whole'}
        ],
        'composition': 'conjunction_contrast',
        'formula': 'And_yet(conjunction=True, contrast=True)',
        'slot_grammar': ['conjunction', 'contrast'],
        'topo_type': 'connection',
        'notes': 'And yet/but - conjunction with contrast/reversal'
    },

    '異': {
        'radicals': [
            {'radical': '田', 'category': 'boundary', 'operation': 'field/grid', 'position': 'bottom'},
            {'radical': '共', 'category': 'action', 'operation': 'together/hands', 'position': 'top'}
        ],
        'composition': 'separate_fields',
        'formula': 'Different(distinct=True, separate=True)',
        'slot_grammar': ['difference', 'distinction'],
        'topo_type': 'P',
        'notes': 'Different/other - separate fields/domains, distinguished'
    },

    '謂': {
        'radicals': [
            {'radical': '言', 'category': 'communication', 'operation': 'speech/words', 'position': 'left'},
            {'radical': '胃', 'category': 'entity', 'operation': 'stomach/organ', 'position': 'right'}
        ],
        'composition': 'speech+containing',
        'formula': 'Call(designation=True, naming=True)',
        'slot_grammar': ['verb', 'designation'],
        'topo_type': 'frame',
        'notes': 'Call/name/say - designate through speech'
    },

    '又': {
        'radicals': [
            {'radical': '又', 'category': 'connection', 'operation': 'again/right_hand', 'position': 'whole'}
        ],
        'composition': 'repetition_hand',
        'formula': 'Again(repetition=True, recursive=True)',
        'slot_grammar': ['adverb', 'repetition'],
        'topo_type': 'connection',
        'notes': 'Again/also - repetition, recursion (玄之又玄 = mystery within mystery)'
    },

    '眾': {
        'radicals': [
            {'radical': '目', 'category': 'perception', 'operation': 'eye/seeing', 'position': 'repeated'},
            {'radical': '人', 'category': 'agent', 'operation': 'people', 'position': 'multiple'}
        ],
        'composition': 'many_people_seeing',
        'formula': 'Multitude(many=True, collective=True)',
        'slot_grammar': ['quantity', 'collective'],
        'topo_type': 'G',
        'notes': 'Multitude/crowd - many entities collectively'
    },

    '門': {
        'radicals': [
            {'radical': '門', 'category': 'boundary', 'operation': 'gate/portal', 'position': 'whole'}
        ],
        'composition': 'double_door_gateway',
        'formula': 'Gate(threshold=True, transition=True)',
        'slot_grammar': ['boundary', 'portal'],
        'topo_type': 'frame',
        'notes': 'Gate/door - threshold between domains, transition portal'
    },

    # === CHAPTER 2 CHARACTERS ===

    '不': {
        'radicals': [
            {'radical': '一', 'category': 'structure', 'operation': 'horizontal/blocking', 'position': 'top'},
            {'radical': '丿', 'category': 'connection', 'operation': 'slash/negation', 'position': 'through'}
        ],
        'composition': 'blocking_stroke',
        'formula': 'Not(negation=True, blocking=True)',
        'slot_grammar': ['negation', 'adverb'],
        'topo_type': 'connection',
        'notes': 'Not - fundamental negation, blocking stroke through horizontal'
    },

    '人': {
        'radicals': [
            {'radical': '人', 'category': 'agent', 'operation': 'person/human', 'position': 'whole'}
        ],
        'composition': 'standing_person',
        'formula': 'Person(agent=True, individual=True)',
        'slot_grammar': ['agent', 'actor'],
        'topo_type': 'P',
        'notes': 'Person/human - individual agent standing upright'
    },

    '美': {
        'radicals': [
            {'radical': '羊', 'category': 'entity', 'operation': 'sheep/offering', 'position': 'top'},
            {'radical': '大', 'category': 'magnitude', 'operation': 'great/expansive', 'position': 'bottom'}
        ],
        'composition': 'great_offering',
        'formula': 'Beautiful(pleasing=True, valuable=True)',
        'slot_grammar': ['quality', 'aesthetic'],
        'topo_type': 'P',
        'notes': 'Beautiful/good - great offering (羊大), aesthetic value'
    },

    '知': {
        'radicals': [
            {'radical': '矢', 'category': 'perception', 'operation': 'arrow/direct', 'position': 'left'},
            {'radical': '口', 'category': 'boundary', 'operation': 'mouth/opening', 'position': 'right'}
        ],
        'composition': 'arrow_to_target',
        'formula': 'Know(direct=True, hit_target=True)',
        'slot_grammar': ['cognition', 'perception'],
        'topo_type': 'perception',
        'notes': 'Know/knowledge - arrow hitting the mark, direct knowing'
    },

    '善': {
        'radicals': [
            {'radical': '羊', 'category': 'entity', 'operation': 'sheep/offering', 'position': 'top'},
            {'radical': '言', 'category': 'communication', 'operation': 'speech/words', 'position': 'bottom'}
        ],
        'composition': 'good_speech',
        'formula': 'Good(virtuous=True, skillful=True)',
        'slot_grammar': ['quality', 'virtue'],
        'topo_type': 'P',
        'notes': 'Good/善 - virtuous speech/action, skillful goodness'
    },

    '惡': {
        'radicals': [
            {'radical': '亞', 'category': 'structure', 'operation': 'secondary/under', 'position': 'top'},
            {'radical': '心', 'category': 'internal', 'operation': 'heart/mind', 'position': 'bottom'}
        ],
        'composition': 'inferior_heart',
        'formula': 'Evil(undesirable=True, inferior=True)',
        'slot_grammar': ['quality', 'negative'],
        'topo_type': 'P',
        'notes': 'Evil/bad - inferior heart/mind, opposite of good'
    },

    '斯': {
        'radicals': [
            {'radical': '其', 'category': 'connection', 'operation': 'this/that', 'position': 'left'},
            {'radical': '斤', 'category': 'action', 'operation': 'axe/cut', 'position': 'right'}
        ],
        'composition': 'cutting_demonstrative',
        'formula': 'Thus(emphatic=True, cutting=True)',
        'slot_grammar': ['demonstrative', 'emphasis'],
        'topo_type': 'connection',
        'notes': 'Thus/then - emphatic demonstrative, cutting to the point'
    },

    '已': {
        'radicals': [
            {'radical': '已', 'category': 'temporal', 'operation': 'already/stop', 'position': 'whole'}
        ],
        'composition': 'completion_marker',
        'formula': 'Already(complete=True, ceased=True)',
        'slot_grammar': ['aspect', 'completion'],
        'topo_type': 'frame',
        'notes': 'Already/stop - completion marker, process ceased'
    },

    '相': {
        'radicals': [
            {'radical': '木', 'category': 'structure', 'operation': 'tree/wood', 'position': 'left'},
            {'radical': '目', 'category': 'perception', 'operation': 'eye/seeing', 'position': 'right'}
        ],
        'composition': 'mutual_seeing',
        'formula': 'Mutual(reciprocal=True, interactive=True)',
        'slot_grammar': ['adverb', 'reciprocal'],
        'topo_type': 'connection',
        'notes': 'Mutual/each other - reciprocal seeing, interactive relationship'
    },

    '生': {
        'radicals': [
            {'radical': '生', 'category': 'transformation', 'operation': 'birth/emerge', 'position': 'whole'}
        ],
        'composition': 'sprouting_emergence',
        'formula': 'Generate(birth=True, emerge=True)',
        'slot_grammar': ['operation', 'emergence'],
        'topo_type': 'G',
        'notes': 'Birth/generate - emergence, sprouting into existence'
    },

    '難': {
        'radicals': [
            {'radical': '隹', 'category': 'entity', 'operation': 'bird/difficult', 'position': 'right'}
        ],
        'composition': 'difficult_bird',
        'formula': 'Difficult(hard=True, complex=True)',
        'slot_grammar': ['quality', 'difficulty'],
        'topo_type': 'P',
        'notes': 'Difficult/hard - complexity, like catching a bird'
    },

    '易': {
        'radicals': [
            {'radical': '日', 'category': 'temporal', 'operation': 'sun/day', 'position': 'top'},
            {'radical': '勿', 'category': 'action', 'operation': 'not/easy', 'position': 'bottom'}
        ],
        'composition': 'sun_rising_easily',
        'formula': 'Easy(simple=True, natural=True)',
        'slot_grammar': ['quality', 'simplicity'],
        'topo_type': 'P',
        'notes': 'Easy/simple - natural like sun rising, opposite of difficult'
    },

    '成': {
        'radicals': [
            {'radical': '丁', 'category': 'structure', 'operation': 'nail/fix', 'position': 'left'},
            {'radical': '戈', 'category': 'action', 'operation': 'weapon/complete', 'position': 'right'}
        ],
        'composition': 'completion_achieved',
        'formula': 'Complete(accomplished=True, finished=True)',
        'slot_grammar': ['operation', 'completion'],
        'topo_type': 'frame',
        'notes': 'Complete/accomplish - achieving fixed result'
    },

    '長': {
        'radicals': [
            {'radical': '長', 'category': 'magnitude', 'operation': 'long/grow', 'position': 'whole'}
        ],
        'composition': 'extended_length',
        'formula': 'Long(extended=True, growing=True)',
        'slot_grammar': ['quality', 'dimension'],
        'topo_type': 'P',
        'notes': 'Long/length - extended in space/time, growing'
    },

    '短': {
        'radicals': [
            {'radical': '矢', 'category': 'perception', 'operation': 'arrow/short', 'position': 'left'},
            {'radical': '豆', 'category': 'entity', 'operation': 'bean/small', 'position': 'right'}
        ],
        'composition': 'short_arrow',
        'formula': 'Short(brief=True, limited=True)',
        'slot_grammar': ['quality', 'dimension'],
        'topo_type': 'P',
        'notes': 'Short/brief - limited extension, opposite of long'
    },

    '形': {
        'radicals': [
            {'radical': '開', 'category': 'action', 'operation': 'open/spread', 'position': 'left'},
            {'radical': '彡', 'category': 'other', 'operation': 'pattern/decoration', 'position': 'right'}
        ],
        'composition': 'visible_pattern',
        'formula': 'Form(shape=True, visible=True)',
        'slot_grammar': ['quality', 'manifestation'],
        'topo_type': 'P',
        'notes': 'Form/shape - visible pattern, manifest structure'
    },

    '高': {
        'radicals': [
            {'radical': '高', 'category': 'magnitude', 'operation': 'tall/high', 'position': 'whole'}
        ],
        'composition': 'elevated_height',
        'formula': 'High(elevated=True, tall=True)',
        'slot_grammar': ['quality', 'dimension'],
        'topo_type': 'P',
        'notes': 'High/tall - elevated position, vertical extension'
    },

    '傾': {
        'radicals': [
            {'radical': '人', 'category': 'agent', 'operation': 'person', 'position': 'left'},
            {'radical': '頃', 'category': 'temporal', 'operation': 'incline/moment', 'position': 'right'}
        ],
        'composition': 'inclining_leaning',
        'formula': 'Incline(tilt=True, lean=True)',
        'slot_grammar': ['operation', 'orientation'],
        'topo_type': 'G',
        'notes': 'Incline/lean - tilting orientation, creating gradient'
    },

    '音': {
        'radicals': [
            {'radical': '立', 'category': 'structure', 'operation': 'stand/establish', 'position': 'top'},
            {'radical': '日', 'category': 'temporal', 'operation': 'sun/day', 'position': 'middle'}
        ],
        'composition': 'established_sound',
        'formula': 'Sound(tone=True, vibration=True)',
        'slot_grammar': ['perception', 'auditory'],
        'topo_type': 'G',
        'notes': 'Sound/tone - established vibration, auditory signal'
    },

    '聲': {
        'radicals': [
            {'radical': '耳', 'category': 'perception', 'operation': 'ear/hearing', 'position': 'bottom'},
            {'radical': '殸', 'category': 'action', 'operation': 'strike/sound', 'position': 'top'}
        ],
        'composition': 'heard_sound',
        'formula': 'Voice(expressed=True, audible=True)',
        'slot_grammar': ['perception', 'communication'],
        'topo_type': 'G',
        'notes': 'Voice/声 - expressed sound reaching ear'
    },

    '和': {
        'radicals': [
            {'radical': '禾', 'category': 'structure', 'operation': 'grain/harmony', 'position': 'left'},
            {'radical': '口', 'category': 'boundary', 'operation': 'mouth/opening', 'position': 'right'}
        ],
        'composition': 'harmonious_grain',
        'formula': 'Harmony(balanced=True, peaceful=True)',
        'slot_grammar': ['quality', 'state'],
        'topo_type': 'O',
        'notes': 'Harmony/peace - balanced like grain, peaceful integration'
    },

    '前': {
        'radicals': [
            {'radical': '刂', 'category': 'action', 'operation': 'knife/cut', 'position': 'right'},
            {'radical': '止', 'category': 'motion', 'operation': 'foot/stop', 'position': 'inside'}
        ],
        'composition': 'forward_cutting',
        'formula': 'Front(ahead=True, forward=True)',
        'slot_grammar': ['position', 'temporal'],
        'topo_type': 'frame',
        'notes': 'Front/before - ahead in space/time, forward direction'
    },

    '後': {
        'radicals': [
            {'radical': '彳', 'category': 'motion', 'operation': 'step/walk', 'position': 'left'},
            {'radical': '幺', 'category': 'structure', 'operation': 'small/thread', 'position': 'right'}
        ],
        'composition': 'following_steps',
        'formula': 'Behind(following=True, after=True)',
        'slot_grammar': ['position', 'temporal'],
        'topo_type': 'frame',
        'notes': 'Behind/after - following position, later in sequence'
    },

    '隨': {
        'radicals': [
            {'radical': '辶', 'category': 'motion', 'operation': 'walking/continuous', 'position': 'surround'},
            {'radical': '隋', 'category': 'other', 'operation': 'follow/yield', 'position': 'inside'}
        ],
        'composition': 'continuous_following',
        'formula': 'Follow(continuous=True, yielding=True)',
        'slot_grammar': ['operation', 'motion'],
        'topo_type': 'G',
        'notes': 'Follow/随 - continuous following motion, yielding to flow'
    },

    '是': {
        'radicals': [
            {'radical': '日', 'category': 'temporal', 'operation': 'sun/correct', 'position': 'top'},
            {'radical': '止', 'category': 'motion', 'operation': 'foot/stop', 'position': 'bottom'}
        ],
        'composition': 'correct_this',
        'formula': 'Is(affirmative=True, correct=True)',
        'slot_grammar': ['copula', 'affirmation'],
        'topo_type': 'connection',
        'notes': 'Is/this - affirmative copula, correct/true'
    },

    '聖': {
        'radicals': [
            {'radical': '耳', 'category': 'perception', 'operation': 'ear/hearing', 'position': 'left'},
            {'radical': '口', 'category': 'boundary', 'operation': 'mouth/speaking', 'position': 'right'}
        ],
        'composition': 'hearing_speaking',
        'formula': 'Sage(wise=True, perceptive=True)',
        'slot_grammar': ['agent', 'wisdom'],
        'topo_type': 'P',
        'notes': 'Sage/saint - wise one who hears and speaks truth'
    },

    '處': {
        'radicals': [
            {'radical': '虍', 'category': 'entity', 'operation': 'tiger/strength', 'position': 'top'},
            {'radical': '夂', 'category': 'motion', 'operation': 'walk/go', 'position': 'bottom'}
        ],
        'composition': 'dwelling_place',
        'formula': 'Dwell(reside=True, position=True)',
        'slot_grammar': ['operation', 'position'],
        'topo_type': 'P',
        'notes': 'Dwell/處 - taking position, residing/handling'
    },

    '事': {
        'radicals': [
            {'radical': '亅', 'category': 'structure', 'operation': 'hook/holding', 'position': 'through'},
            {'radical': '口', 'category': 'boundary', 'operation': 'boundary/affair', 'position': 'core'}
        ],
        'composition': 'managed_affair',
        'formula': 'Affair(matter=True, managed=True)',
        'slot_grammar': ['entity', 'action'],
        'topo_type': 'P',
        'notes': 'Affair/matter - managed business, thing to be done'
    },

    '行': {
        'radicals': [
            {'radical': '彳', 'category': 'motion', 'operation': 'step/walk', 'position': 'left'},
            {'radical': '亍', 'category': 'motion', 'operation': 'step/walk', 'position': 'right'}
        ],
        'composition': 'walking_steps',
        'formula': 'Walk(move=True, practice=True)',
        'slot_grammar': ['operation', 'motion'],
        'topo_type': 'G',
        'notes': 'Walk/practice/行 - continuous walking, putting into practice'
    },

    '言': {
        'radicals': [
            {'radical': '言', 'category': 'communication', 'operation': 'speech/words', 'position': 'whole'}
        ],
        'composition': 'spoken_words',
        'formula': 'Speak(words=True, verbal=True)',
        'slot_grammar': ['communication', 'verbal'],
        'topo_type': 'G',
        'notes': 'Speech/words - verbal communication, spoken language'
    },

    '教': {
        'radicals': [
            {'radical': '孝', 'category': 'entity', 'operation': 'filial/teach', 'position': 'left'},
            {'radical': '攴', 'category': 'action', 'operation': 'strike/tap', 'position': 'right'}
        ],
        'composition': 'teaching_instruction',
        'formula': 'Teach(instruct=True, guide=True)',
        'slot_grammar': ['operation', 'transmission'],
        'topo_type': 'G',
        'notes': 'Teach/instruct - guiding instruction, transmitted knowledge'
    },

    '作': {
        'radicals': [
            {'radical': '人', 'category': 'agent', 'operation': 'person', 'position': 'left'},
            {'radical': '乍', 'category': 'action', 'operation': 'sudden/make', 'position': 'right'}
        ],
        'composition': 'person_making',
        'formula': 'Make(create=True, arise=True)',
        'slot_grammar': ['operation', 'creation'],
        'topo_type': 'G',
        'notes': 'Make/arise - creative action, things arising'
    },

    '焉': {
        'radicals': [
            {'radical': '焉', 'category': 'other', 'operation': 'how/where/therein', 'position': 'whole'}
        ],
        'composition': 'modal_particle',
        'formula': 'Therein(modal=True, location=True)',
        'slot_grammar': ['particle', 'modal'],
        'topo_type': 'connection',
        'notes': 'Therein/how - modal particle indicating manner/location'
    },

    '辭': {
        'radicals': [
            {'radical': '辛', 'category': 'other', 'operation': 'bitter/decline', 'position': 'left'},
            {'radical': '言', 'category': 'communication', 'operation': 'words/speech', 'position': 'right'}
        ],
        'composition': 'declining_words',
        'formula': 'Decline(refuse=True, resign=True)',
        'slot_grammar': ['operation', 'refusal'],
        'topo_type': 'connection',
        'notes': 'Decline/辭 - refusing credit, resigning from claim'
    },

    '恃': {
        'radicals': [
            {'radical': '心', 'category': 'internal', 'operation': 'heart/mind', 'position': 'left'},
            {'radical': '寺', 'category': 'structure', 'operation': 'temple/rely', 'position': 'right'}
        ],
        'composition': 'heart_relying',
        'formula': 'Rely(depend=True, presume=True)',
        'slot_grammar': ['operation', 'dependence'],
        'topo_type': 'connection',
        'notes': 'Rely/presume - depending on, presuming upon'
    },

    '功': {
        'radicals': [
            {'radical': '工', 'category': 'action', 'operation': 'work/construct', 'position': 'left'},
            {'radical': '力', 'category': 'action', 'operation': 'strength/power', 'position': 'right'}
        ],
        'composition': 'work_power',
        'formula': 'Merit(achievement=True, work_done=True)',
        'slot_grammar': ['entity', 'accomplishment'],
        'topo_type': 'P',
        'notes': 'Merit/achievement - work accomplished through power'
    },

    '弗': {
        'radicals': [
            {'radical': '弓', 'category': 'action', 'operation': 'bow/curved', 'position': 'outside'},
            {'radical': '⼃', 'category': 'structure', 'operation': 'slash/not', 'position': 'through'}
        ],
        'composition': 'bow_negation',
        'formula': 'Not(emphatic=True, negative=True)',
        'slot_grammar': ['negation', 'emphasis'],
        'topo_type': 'connection',
        'notes': 'Not/弗 - emphatic negation, stronger than 不'
    },

    '居': {
        'radicals': [
            {'radical': '尸', 'category': 'constraint', 'operation': 'dwelling/body', 'position': 'surround'},
            {'radical': '古', 'category': 'temporal', 'operation': 'ancient/old', 'position': 'inside'}
        ],
        'composition': 'dwelling_residence',
        'formula': 'Dwell(reside=True, remain=True)',
        'slot_grammar': ['operation', 'position'],
        'topo_type': 'P',
        'notes': 'Dwell/reside/居 - remaining in position, taking credit'
    },

    '夫': {
        'radicals': [
            {'radical': '大', 'category': 'magnitude', 'operation': 'great/large', 'position': 'base'},
            {'radical': '一', 'category': 'structure', 'operation': 'horizontal/top', 'position': 'above'}
        ],
        'composition': 'mature_man',
        'formula': 'Man(mature=True, husband=True)',
        'slot_grammar': ['agent', 'particle'],
        'topo_type': 'P',
        'notes': 'Man/husband/夫 - mature male, also exclamatory particle'
    },

    '唯': {
        'radicals': [
            {'radical': '口', 'category': 'boundary', 'operation': 'mouth/speech', 'position': 'left'},
            {'radical': '隹', 'category': 'entity', 'operation': 'bird/only', 'position': 'right'}
        ],
        'composition': 'only_response',
        'formula': 'Only(exclusive=True, unique=True)',
        'slot_grammar': ['adverb', 'limitation'],
        'topo_type': 'frame',
        'notes': 'Only/solely/唯 - exclusive limitation, unique response'
    },

    '去': {
        'radicals': [
            {'radical': '土', 'category': 'structure', 'operation': 'earth/ground', 'position': 'top'},
            {'radical': '厶', 'category': 'structure', 'operation': 'private/self', 'position': 'bottom'}
        ],
        'composition': 'departing_leaving',
        'formula': 'Leave(depart=True, go_away=True)',
        'slot_grammar': ['operation', 'motion'],
        'topo_type': 'G',
        'notes': 'Leave/depart - going away, removing from position'
    },

    '皆': {
        'radicals': [
            {'radical': '比', 'category': 'connection', 'operation': 'compare/together', 'position': 'top'},
            {'radical': '白', 'category': 'other', 'operation': 'white/clear', 'position': 'bottom'}
        ],
        'composition': 'all_together',
        'formula': 'All(universal=True, collective=True)',
        'slot_grammar': ['adverb', 'universal'],
        'topo_type': 'frame',
        'notes': 'All/universally - everyone/everything together, collective totality'
    },
}


# Structural Pattern Templates
PATTERN_TEMPLATES = {
    'P_O_G': {
        'name': 'Perimeter → Origin → Gradient',
        'description': 'Boundary creates void which generates emergence',
        'formula': 'Boundary(P) → Void(O) → Emergence(G)',
        'examples': ['Chapter 11 wheel', 'Chapter 11 vessel', 'Chapter 11 room']
    },

    'O_G_P': {
        'name': 'Origin → Gradient → Perimeter',
        'description': 'Source generates flow that creates boundary',
        'formula': 'Source(O) → Flow(G) → Boundary(P)',
        'examples': ['Chapter 1 naming', 'Chapter 4 Tao emergence']
    },

    'transformation_pair': {
        'name': 'Absence-Action Transformation Pair',
        'description': 'Two modes of transformation (無/為)',
        'formula': 'Transform(absence) ⟷ Transform(action)',
        'examples': ['無為 wu-wei', 'Chapter 2 contrasts']
    },

    'recursive_cycle': {
        'name': 'Recursive Return Cycle',
        'description': 'Process that returns to origin (反者道之動)',
        'formula': 'O → G → P → O₂',
        'examples': ['Chapter 25 great-passing-far-returning', 'Chapter 16 return to root']
    }
}


class TranslationEngine:
    """Multi-layer translation engine for Dao De Jing"""

    def __init__(self):
        self.character_db = CHARACTER_OPERATIONS
        self.pattern_templates = PATTERN_TEMPLATES

    def analyze_character(self, char: str) -> Optional[CharacterStructure]:
        """Get complete structural analysis of a character"""
        if char not in self.character_db:
            return None

        data = self.character_db[char]

        radical_ops = [
            RadicalOperation(
                radical=r['radical'],
                category=r['category'],
                operation=r['operation'],
                position=r['position']
            )
            for r in data['radicals']
        ]

        return CharacterStructure(
            char=char,
            radicals=radical_ops,
            composition=data['composition'],
            structural_formula=data['formula'],
            slot_grammar=data['slot_grammar'],
            topological_type=data['topo_type']
        )

    def translate_multilayer(self, text: str, context: Dict = None) -> List[TranslationLayer]:
        """
        Generate multi-layer translation of a text passage

        Args:
            text: Chinese text to translate
            context: Chapter number, position, etc.

        Returns:
            List of translation layers (surface, operational, structural, pattern)
        """
        layers = []

        # Layer 1: Character breakdown
        char_breakdown = self._layer_character_breakdown(text)
        layers.append(TranslationLayer(
            level="character_breakdown",
            content=char_breakdown,
            annotations={}
        ))

        # Layer 2: Radical operations
        radical_ops = self._layer_radical_operations(text)
        layers.append(TranslationLayer(
            level="radical_operations",
            content=radical_ops,
            annotations={}
        ))

        # Layer 3: Structural mechanics
        structural = self._layer_structural_mechanics(text)
        layers.append(TranslationLayer(
            level="structural_mechanics",
            content=structural,
            annotations={}
        ))

        # Layer 4: Pattern recognition
        patterns = self._layer_pattern_recognition(text)
        layers.append(TranslationLayer(
            level="pattern_recognition",
            content=patterns,
            annotations={}
        ))

        return layers

    def _layer_character_breakdown(self, text: str) -> str:
        """Layer 1: Show each character with its radicals"""
        breakdown = []

        for char in text:
            if char in self.character_db:
                data = self.character_db[char]
                rad_str = "+".join([r['radical'] for r in data['radicals']])
                breakdown.append(f"{char}[{rad_str}]")
            else:
                breakdown.append(char)

        return " ".join(breakdown)

    def _layer_radical_operations(self, text: str) -> str:
        """Layer 2: Show what each radical is DOING"""
        operations = []

        for char in text:
            if char in self.character_db:
                data = self.character_db[char]
                ops = " + ".join([r['operation'] for r in data['radicals']])
                operations.append(f"{char}: [{ops}]")
            else:
                operations.append(char)

        return "\n".join(operations)

    def _layer_structural_mechanics(self, text: str) -> str:
        """Layer 3: Show the structural formula"""
        formulas = []

        for char in text:
            if char in self.character_db:
                data = self.character_db[char]
                formulas.append(f"{char} = {data['formula']}")
            else:
                formulas.append(char)

        return "\n".join(formulas)

    def _layer_pattern_recognition(self, text: str) -> str:
        """Layer 4: Identify structural patterns in the sequence"""
        # Get topological types for each character
        topo_sequence = []

        for char in text:
            if char in self.character_db:
                topo_sequence.append(self.character_db[char]['topo_type'])
            else:
                topo_sequence.append('?')

        pattern_str = " → ".join(topo_sequence)

        # Check for known patterns
        detected_patterns = []
        if 'O' in topo_sequence and 'G' in topo_sequence and 'P' in topo_sequence:
            detected_patterns.append("O→G→P cycle detected")

        if '無' in text and '為' in text:
            detected_patterns.append("Transformation pair (無/為) detected")

        result = f"Topological sequence: {pattern_str}\n"
        if detected_patterns:
            result += "Patterns detected:\n" + "\n".join(f"  - {p}" for p in detected_patterns)

        return result


if __name__ == "__main__":
    engine = TranslationEngine()

    # Test with Chapter 1 opening
    print("="*80)
    print("TRANSLATION ENGINE TEST - Chapter 1 Opening")
    print("="*80)

    test_passages = [
        ("道可道", "The Tao that can be told"),
        ("非常道", "Is not the eternal Tao"),
        ("名可名", "The name that can be named"),
        ("非常名", "Is not the eternal name"),
        ("無名天地之始", "The nameless is the beginning of heaven and earth"),
        ("有名萬物之母", "The named is the mother of ten thousand things"),
    ]

    for chinese, traditional in test_passages:
        print(f"\n{'─'*80}")
        print(f"Text: {chinese}")
        print(f"Traditional: {traditional}")
        print(f"{'─'*80}\n")

        layers = engine.translate_multilayer(chinese)

        for layer in layers:
            print(f"[{layer.level.upper().replace('_', ' ')}]")
            print(layer.content)
            print()

    # Test individual character analysis
    print("\n" + "="*80)
    print("DETAILED CHARACTER ANALYSIS")
    print("="*80)

    test_chars = ['道', '無', '為', '有', '名', '常']

    for char in test_chars:
        structure = engine.analyze_character(char)
        if structure:
            print(f"\n{char} ({CHARACTER_OPERATIONS[char]['notes']}):")
            print(f"  Radicals: {', '.join([r.radical for r in structure.radicals])}")
            print(f"  Operations: {', '.join([r.operation for r in structure.radicals])}")
            print(f"  Composition: {structure.composition}")
            print(f"  Formula: {structure.structural_formula}")
            print(f"  Topological type: {structure.topological_type}")
            print(f"  Grammar slots: {', '.join(structure.slot_grammar)}")
