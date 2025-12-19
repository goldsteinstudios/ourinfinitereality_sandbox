"""
AgriculturalFeatureExtractor: Features for testing the agricultural hypothesis.

This module contains feature extractors specifically designed to test
whether Chu bamboo slip characters support agricultural pictographic
interpretations vs. standard etymological decompositions.

Key hypothesis being tested:
- Many characters preserve agricultural imagery from early farming communities
- Standard radical decompositions may obscure original pictographic content
- CHUBS glyphs may show features not visible in later standardized forms
"""

from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
import json

# Optional dependencies
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    np = None

from .image_processor import GlyphImageProcessor


class AgriculturalFeatureExtractor:
    """
    Extract features that distinguish agricultural from standard interpretations.

    For each Tier 1 character, we define specific visual features that would
    support or refute the agricultural hypothesis.

    Example for 道:
    - Standard: 辶 (movement) + 首 (head) = "way/path led by the head/chief"
    - Agricultural: Walking figure + water vessel = "carrying water along irrigation path"

    We look for:
    - Vessel curvature in upper component (supports agricultural)
    - Facial features in upper component (supports standard)
    - Walking vs. abstract motion in lower component
    """

    # Hypothesis definitions for Tier 1 characters
    TIER_1_HYPOTHESES = {
        "道": {
            "standard": {
                "claim": "Upper component is 首 (head/chief), lower is 辶 (movement)",
                "features_to_detect": ["facial_features", "abstract_motion"]
            },
            "agricultural": {
                "claim": "Upper component depicts water vessel on carrying pole",
                "features_to_detect": ["vessel_curvature", "carrying_pole", "walking_stance"]
            },
            "falsification": {
                "agricultural_threshold": "If <30% of exemplars show vessel curvature, hypothesis weakened",
                "standard_threshold": "If >70% show clear facial features, agricultural hypothesis refuted"
            }
        },
        "德": {
            "standard": {
                "claim": "彳 (step) + 直 (straight) + 心 (heart) = virtue/alignment",
                "features_to_detect": ["heart_component", "straight_line"]
            },
            "agricultural": {
                "claim": "Movement toward aligned planting rows",
                "features_to_detect": ["row_alignment", "directional_motion"]
            },
            "falsification": {}
        },
        "自": {
            "standard": {
                "claim": "Pictograph of nose, hence 'self' from pointing at nose",
                "features_to_detect": ["nostril_holes", "nose_bridge", "facial_profile"]
            },
            "agricultural": {
                "claim": "Seed or grain kernel pictograph",
                "features_to_detect": ["seed_shape", "pointed_base", "rounded_top"]
            },
            "falsification": {
                "standard_threshold": "If >60% show clear nostril features, seed hypothesis refuted",
                "note": "Counter-evidence: smell-related compounds (息, 鼻, 臭, 嗅)"
            }
        },
        "反": {
            "standard": {
                "claim": "又 (hand) + 厂 (cliff) = turning hand against cliff",
                "features_to_detect": ["hand_shape", "cliff_overhang"]
            },
            "agricultural": {
                "claim": "Overturning/reversing motion (plowing, turning soil)",
                "features_to_detect": ["turning_motion", "curved_trajectory"]
            },
            "falsification": {}
        },
        "弱": {
            "standard": {
                "claim": "Two 弓 (bows) = weak/yielding",
                "features_to_detect": ["double_bow", "symmetry"]
            },
            "agricultural": {
                "claim": "Young plants/sprouts bending",
                "features_to_detect": ["plant_stems", "bending_form", "organic_curves"]
            },
            "falsification": {}
        },
        "者": {
            "standard": {
                "claim": "耂 (old) variant + 日 = one who/that which",
                "features_to_detect": ["sun_element", "person_element"]
            },
            "agricultural": {
                "claim": "Container/vessel marker (that which contains)",
                "features_to_detect": ["container_shape", "enclosure"]
            },
            "falsification": {}
        }
    }

    def __init__(self, processor: Optional[GlyphImageProcessor] = None):
        """
        Initialize the extractor.

        Args:
            processor: GlyphImageProcessor instance
        """
        self.processor = processor or GlyphImageProcessor()
        self.project_root = Path(__file__).parent.parent.parent

    def analyze_character(
        self,
        character: str,
        exemplar_paths: Optional[List[Path]] = None,
        manual_assessment: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze a character for agricultural vs. standard features.

        Args:
            character: The Chinese character
            exemplar_paths: Specific images to analyze (or auto-select)
            manual_assessment: Include prompts for manual visual assessment

        Returns:
            Analysis result with feature scores and hypothesis comparison
        """
        if character not in self.TIER_1_HYPOTHESES:
            return {
                "character": character,
                "error": f"No hypothesis defined for {character}",
                "is_tier_1": False
            }

        hypothesis = self.TIER_1_HYPOTHESES[character]

        # Get exemplar images
        if exemplar_paths is None:
            exemplar_paths = self.processor.list_glyph_images(character)[:5]

        result = {
            "character": character,
            "is_tier_1": True,
            "exemplar_count": len(exemplar_paths),
            "standard_hypothesis": hypothesis["standard"]["claim"],
            "agricultural_hypothesis": hypothesis["agricultural"]["claim"],
            "falsification_criteria": hypothesis.get("falsification", {}),
            "automated_features": {},
            "manual_assessment_prompts": [],
            "verdict": None
        }

        # Automated feature extraction (basic)
        if HAS_NUMPY and exemplar_paths:
            result["automated_features"] = self._extract_automated_features(
                character, exemplar_paths
            )

        # Manual assessment prompts
        if manual_assessment:
            result["manual_assessment_prompts"] = self._generate_assessment_prompts(
                character, hypothesis
            )

        return result

    def _extract_automated_features(
        self,
        character: str,
        exemplar_paths: List[Path]
    ) -> Dict[str, Any]:
        """
        Extract automated features from exemplar images.

        Currently basic; to be enhanced with contour analysis.
        """
        features = {
            "image_count": len(exemplar_paths),
            "quality_scores": [],
            "size_variance": None,
            "contrast_scores": []
        }

        for path in exemplar_paths:
            score = self.processor.get_image_quality_score(path)
            features["quality_scores"].append(score)

        if features["quality_scores"]:
            features["avg_quality"] = sum(features["quality_scores"]) / len(features["quality_scores"])

        return features

    def _generate_assessment_prompts(
        self,
        character: str,
        hypothesis: Dict
    ) -> List[Dict[str, str]]:
        """
        Generate prompts for manual visual assessment.
        """
        prompts = []

        # Standard features
        for feature in hypothesis["standard"].get("features_to_detect", []):
            prompts.append({
                "hypothesis": "standard",
                "feature": feature,
                "question": self._feature_to_question(feature, "standard"),
                "response_type": "scale_1_5"
            })

        # Agricultural features
        for feature in hypothesis["agricultural"].get("features_to_detect", []):
            prompts.append({
                "hypothesis": "agricultural",
                "feature": feature,
                "question": self._feature_to_question(feature, "agricultural"),
                "response_type": "scale_1_5"
            })

        return prompts

    def _feature_to_question(self, feature: str, hypothesis: str) -> str:
        """Convert feature name to assessment question."""
        questions = {
            # Standard features
            "facial_features": "Do you see recognizable facial features (eyes, nose, mouth)?",
            "abstract_motion": "Does the lower component appear as abstract motion marks?",
            "heart_component": "Is there a clear heart (心) component?",
            "straight_line": "Is there a prominent straight/vertical line?",
            "nostril_holes": "Do you see two holes that could represent nostrils?",
            "nose_bridge": "Is there a vertical line that could be a nose bridge?",
            "facial_profile": "Does the shape suggest a face in profile?",
            "hand_shape": "Do you see a clear hand shape?",
            "cliff_overhang": "Is there an overhanging cliff-like element?",
            "double_bow": "Do you see two bow-shaped elements?",
            "symmetry": "Is the character roughly symmetrical?",
            "sun_element": "Is there a sun/circle element?",
            "person_element": "Is there a person-like element?",

            # Agricultural features
            "vessel_curvature": "Does the upper component show bowl/vessel-like curvature?",
            "carrying_pole": "Is there a vertical element that could be a carrying pole?",
            "walking_stance": "Does the lower component show a walking figure stance?",
            "row_alignment": "Do you see parallel lines suggesting planted rows?",
            "directional_motion": "Is there clear directional movement indicated?",
            "seed_shape": "Does the shape resemble a seed or grain kernel?",
            "pointed_base": "Is there a pointed base (like a seed)?",
            "rounded_top": "Is the top rounded (like a seed)?",
            "turning_motion": "Does the shape suggest a turning/overturning motion?",
            "curved_trajectory": "Is there a curved path or trajectory?",
            "plant_stems": "Do you see elements that could be plant stems?",
            "bending_form": "Does the form show bending or yielding?",
            "organic_curves": "Are the curves organic rather than geometric?",
            "container_shape": "Does the overall shape suggest a container?",
            "enclosure": "Is there an enclosing or containing element?"
        }

        return questions.get(feature, f"Rate the presence of '{feature}'")

    def record_manual_assessment(
        self,
        character: str,
        assessments: Dict[str, int],
        assessor: str = "anonymous"
    ) -> Dict[str, Any]:
        """
        Record manual visual assessment results.

        Args:
            character: The Chinese character
            assessments: Dict mapping feature names to scores (1-5)
            assessor: Who performed the assessment

        Returns:
            Processed assessment with hypothesis scores
        """
        if character not in self.TIER_1_HYPOTHESES:
            return {"error": f"No hypothesis for {character}"}

        hypothesis = self.TIER_1_HYPOTHESES[character]

        # Calculate scores for each hypothesis
        standard_features = hypothesis["standard"].get("features_to_detect", [])
        agricultural_features = hypothesis["agricultural"].get("features_to_detect", [])

        standard_scores = [assessments.get(f, 0) for f in standard_features]
        agricultural_scores = [assessments.get(f, 0) for f in agricultural_features]

        standard_avg = sum(standard_scores) / len(standard_scores) if standard_scores else 0
        agricultural_avg = sum(agricultural_scores) / len(agricultural_scores) if agricultural_scores else 0

        # Normalize to 0-1
        standard_score = standard_avg / 5
        agricultural_score = agricultural_avg / 5

        # Determine verdict
        if agricultural_score > standard_score + 0.2:
            verdict = "agricultural_supported"
        elif standard_score > agricultural_score + 0.2:
            verdict = "standard_supported"
        else:
            verdict = "inconclusive"

        return {
            "character": character,
            "assessor": assessor,
            "standard_score": standard_score,
            "agricultural_score": agricultural_score,
            "verdict": verdict,
            "raw_assessments": assessments,
            "feature_breakdown": {
                "standard": dict(zip(standard_features, standard_scores)),
                "agricultural": dict(zip(agricultural_features, agricultural_scores))
            }
        }

    def compare_hypotheses(self, character: str) -> Dict[str, Any]:
        """
        Generate a comparison report for the two hypotheses.

        Args:
            character: The Chinese character

        Returns:
            Comparison report
        """
        if character not in self.TIER_1_HYPOTHESES:
            return {"error": f"No hypothesis for {character}"}

        h = self.TIER_1_HYPOTHESES[character]

        return {
            "character": character,
            "standard": {
                "claim": h["standard"]["claim"],
                "features": h["standard"]["features_to_detect"]
            },
            "agricultural": {
                "claim": h["agricultural"]["claim"],
                "features": h["agricultural"]["features_to_detect"]
            },
            "falsification": h.get("falsification", {}),
            "status": "awaiting_analysis"
        }

    def get_all_tier_1_status(self) -> Dict[str, Any]:
        """
        Get analysis status for all Tier 1 characters.

        Returns:
            Status summary
        """
        status = {}
        for char in self.TIER_1_HYPOTHESES.keys():
            images = self.processor.list_glyph_images(char)
            status[char] = {
                "hypothesis_defined": True,
                "image_count": len(images),
                "analysis_complete": False,  # Would check for saved assessments
                "verdict": None
            }

        return {
            "tier_1_characters": list(self.TIER_1_HYPOTHESES.keys()),
            "status": status,
            "total_defined": len(self.TIER_1_HYPOTHESES),
            "total_analyzed": 0  # Would count completed analyses
        }


def main():
    """Test the feature extractor."""
    extractor = AgriculturalFeatureExtractor()

    print("=== Agricultural Feature Extractor ===")
    print()

    # Show all Tier 1 hypotheses
    print("Tier 1 Hypothesis Summary:")
    print("-" * 60)

    for char, hyp in extractor.TIER_1_HYPOTHESES.items():
        print(f"\n{char}:")
        print(f"  Standard: {hyp['standard']['claim']}")
        print(f"  Agricultural: {hyp['agricultural']['claim']}")
        if hyp.get('falsification'):
            for key, val in hyp['falsification'].items():
                print(f"  Falsification ({key}): {val}")

    # Analyze one character
    print()
    print("=" * 60)
    print("Sample analysis for 道:")
    result = extractor.analyze_character("道")
    print(f"  Exemplars available: {result['exemplar_count']}")
    print(f"  Assessment prompts: {len(result['manual_assessment_prompts'])}")

    # Show prompts
    print("\n  Manual assessment questions:")
    for p in result['manual_assessment_prompts'][:4]:
        print(f"    [{p['hypothesis']}] {p['question']}")


if __name__ == "__main__":
    main()
