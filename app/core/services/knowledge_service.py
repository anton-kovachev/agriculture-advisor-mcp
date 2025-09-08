from typing import List, Dict, Any
from datetime import datetime
from app.core.models.crop import CropType, GrowthStage
from app.core.models.location import GeoLocation


class KnowledgeBaseService:
    """Service for managing and retrieving agricultural knowledge and recommendations."""

    def __init__(self):
        # Initialize disease risk factors for different crops
        self._disease_risk_factors = {
            CropType.WHEAT: {
                "black_rust": {
                    "temp_range": (15, 25),
                    "humidity_range": (60, 100),
                    "risk_description": "High risk when temperature is between 15-25°C with high humidity",
                    "symptoms": [
                        "Reddish-brown pustules on leaves and stems",
                        "Black teliospores form late in season",
                        "Reduced grain fill and yield"
                    ],
                    "management": [
                        "Plant resistant varieties",
                        "Early planting to avoid peak disease period",
                        "Monitor and apply fungicides when necessary"
                    ]
                },
                "smut": {
                    "temp_range": (16, 22),
                    "humidity_range": (70, 100),
                    "risk_description": "Risk increases with high humidity and moderate temperatures",
                    "symptoms": [
                        "Black spores replace grain in heads",
                        "Fishy smell in infected grain",
                        "Reduced grain quality"
                    ],
                    "management": [
                        "Use certified disease-free seed",
                        "Treat seeds with fungicide",
                        "Practice crop rotation"
                    ]
                },
                "powdery_mildew": {
                    "temp_range": (15, 22),
                    "humidity_range": (50, 100),
                    "risk_description": "Common in dense canopies with high humidity",
                    "symptoms": [
                        "White powdery growth on leaves",
                        "Yellowing and death of leaves",
                        "Reduced photosynthesis"
                    ],
                    "management": [
                        "Use resistant varieties",
                        "Maintain good air circulation",
                        "Apply fungicides preventively in high-risk conditions"
                    ]
                }
            },
            CropType.CORN: {
                "northern_leaf_blight": {
                    "temp_range": (18, 27),
                    "humidity_range": (70, 100),
                    "risk_description": "Favored by moderate temperatures and high humidity",
                    "symptoms": [
                        "Long, cigar-shaped lesions",
                        "Grayish-green to brown color",
                        "Lesions begin on lower leaves"
                    ],
                    "management": [
                        "Plant resistant hybrids",
                        "Rotate crops",
                        "Apply fungicides at early infection"
                    ]
                },
                "gray_leaf_spot": {
                    "temp_range": (22, 30),
                    "humidity_range": (85, 100),
                    "risk_description": "Severe in areas with high humidity and warm temperatures",
                    "symptoms": [
                        "Rectangular lesions between leaf veins",
                        "Gray to tan color",
                        "Lesions expand and coalesce"
                    ],
                    "management": [
                        "Use resistant hybrids",
                        "Practice crop rotation",
                        "Consider fungicide application"
                    ]
                },
                "common_rust": {
                    "temp_range": (16, 25),
                    "humidity_range": (75, 100),
                    "risk_description": "Develops rapidly in cool, moist conditions",
                    "symptoms": [
                        "Small, circular pustules on leaves",
                        "Reddish-brown color",
                        "Pustules on both leaf surfaces"
                    ],
                    "management": [
                        "Plant resistant hybrids",
                        "Monitor fields regularly",
                        "Apply fungicides if detected early"
                    ]
                }
            }
        }

        # Initialize protection strategies database
        self._protection_strategies = {
            "disease_control": {
                "chemical": {
                    "fungicides": "Apply appropriate fungicides when disease risk is high",
                    "seed_treatment": "Treat seeds with fungicides before planting"
                },
                "cultural": {
                    "crop_rotation": "Rotate crops to break disease cycles",
                    "resistant_varieties": "Use disease-resistant varieties when available"
                }
            },
            "pest_control": {
                "chemical": {
                    "insecticides": "Apply insecticides when pest thresholds are exceeded"
                },
                "biological": {
                    "beneficial_insects": "Encourage natural predators",
                    "trap_crops": "Plant trap crops to protect main crop"
                }
            },
            "weed_control": {
                "chemical": {
                    "herbicides": "Use selective herbicides appropriate for the crop"
                },
                "mechanical": {
                    "tillage": "Implement appropriate tillage practices",
                    "mulching": "Use mulch to suppress weed growth"
                }
            }
        }

    def get_disease_risks(
        self,
        crop_type: CropType,
        temperature: float,
        humidity: float
    ) -> List[Dict[str, Any]]:
        """
        Evaluate potential disease risks based on current conditions.
        """
        risks = []
        if crop_type in self._disease_risk_factors:
            for disease, factors in self._disease_risk_factors[crop_type].items():
                temp_min, temp_max = factors["temp_range"]
                humidity_min, humidity_max = factors["humidity_range"]

                if (temp_min <= temperature <= temp_max and
                        humidity_min <= humidity <= humidity_max):
                    risks.append({
                        "disease": disease,
                        "risk_level": "high",
                        "description": factors["risk_description"],
                        "contributing_factors": {
                            "temperature": temperature,
                            "humidity": humidity
                        }
                    })

        return risks

    def get_protection_measures(
        self,
        crop_type: CropType,
        growth_stage: GrowthStage,
        conditions: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """
        Get recommended protection measures based on crop type, growth stage, and conditions.
        """
        recommendations = {
            "disease_control": [],
            "pest_control": [],
            "weed_control": []
        }

        # Add disease control recommendations
        if growth_stage in [GrowthStage.EMERGENCE, GrowthStage.TILLERING]:
            recommendations["disease_control"].extend([
                self._protection_strategies["disease_control"]["cultural"]["crop_rotation"],
                self._protection_strategies["disease_control"]["chemical"]["seed_treatment"]
            ])

        # Add pest control recommendations
        if growth_stage in [GrowthStage.EMERGENCE, GrowthStage.FLOWERING]:
            recommendations["pest_control"].extend([
                self._protection_strategies["pest_control"]["biological"]["beneficial_insects"],
                self._protection_strategies["pest_control"]["chemical"]["insecticides"]
            ])

        # Add weed control recommendations
        if growth_stage in [GrowthStage.EMERGENCE, GrowthStage.TILLERING]:
            recommendations["weed_control"].extend([
                self._protection_strategies["weed_control"]["mechanical"]["tillage"],
                self._protection_strategies["weed_control"]["chemical"]["herbicides"]
            ])

        return recommendations

    def get_farming_techniques(
        self,
        crop_type: CropType,
        climate_zone: str,
        soil_type: str
    ) -> Dict[str, Any]:
        """
        Get recommended farming techniques based on crop type and local conditions.
        """
        base_techniques = {
            CropType.SUNFLOWER: {
                "soil_preparation": {
                    "tillage_depth": "20-25cm",
                    "primary_tillage": "Deep plowing in fall",
                    "secondary_tillage": "Light cultivation before planting",
                    "soil_requirements": {
                        "optimal_ph": "6.0-7.5",
                        "organic_matter": ">1.5%",
                        "drainage": "Well-drained soils essential"
                    },
                    "recommended_methods": [
                        "Deep tillage to break hardpan",
                        "Seedbed should be firm and level",
                        "Avoid excessive tillage to prevent soil moisture loss"
                    ]
                },
                "planting": {
                    "timing": {
                        "soil_temperature": "Above 8°C (46°F)",
                        "frost_risk": "After all danger of spring frost",
                        "season": "Early spring to early summer"
                    },
                    "seed_depth": "4-6cm",
                    "row_spacing": "70-100cm",
                    "plant_spacing": "20-30cm",
                    "seeding_rate": "40,000-50,000 seeds/ha",
                    "considerations": [
                        "Plant when soil is moist but not wet",
                        "Consider bee population for pollination",
                        "Avoid planting in areas with bird pressure"
                    ]
                },
                "fertilization": {
                    "base_application": {
                        "npk_ratio": "20-40-40",
                        "timing": "Pre-planting incorporation",
                        "method": "Broadcast and incorporate"
                    },
                    "nutrient_requirements": {
                        "nitrogen": "60-100 kg/ha",
                        "phosphorus": "40-80 kg/ha",
                        "potassium": "40-80 kg/ha",
                        "boron": "1-2 kg/ha if deficient"
                    },
                    "timing": [
                        "50% at planting",
                        "50% at V4 stage (4 true leaves)"
                    ]
                },
                "irrigation": {
                    "critical_periods": [
                        "Germination to emergence",
                        "Flowering",
                        "Seed filling"
                    ],
                    "water_requirements": "400-500mm total",
                    "methods": [
                        "Center pivot irrigation",
                        "Drip irrigation for water conservation"
                    ],
                    "management": {
                        "early_stage": "Maintain consistent moisture",
                        "flowering": "Critical irrigation period",
                        "maturity": "Reduce irrigation for proper drying"
                    }
                },
                "harvest": {
                    "timing": {
                        "moisture_content": "Below 12%",
                        "indicators": [
                            "Back of head turns brown",
                            "Bracts turn brown",
                            "Seeds are firm and dark"
                        ]
                    },
                    "methods": [
                        "Combine harvesting",
                        "Adjust combine settings to minimize damage"
                    ],
                    "post_harvest": [
                        "Quick drying if moisture is above 10%",
                        "Clean storage facilities",
                        "Monitor temperature and moisture during storage"
                    ]
                }
            },
            CropType.CORN: {
                "soil_preparation": {
                    "tillage_depth": "20-30cm",
                    "primary_tillage": "Fall plowing recommended for heavy soils",
                    "secondary_tillage": "Spring cultivation to prepare seedbed",
                    "soil_requirements": {
                        "optimal_ph": "6.0-7.0",
                        "organic_matter": ">2%",
                        "drainage": "Well-drained soils required"
                    },
                    "recommended_methods": [
                        "Deep plowing for heavy soils",
                        "Conservation tillage for erosion-prone areas",
                        "Minimum tillage in dry regions"
                    ]
                },
                "planting": {
                    "timing": {
                        "soil_temperature": "Above 10°C (50°F)",
                        "frost_risk": "Plant after last spring frost"
                    },
                    "seed_depth": "5-7cm",
                    "row_spacing": "75-100cm",
                    "plant_spacing": "15-20cm",
                    "seeding_rate": "60,000-70,000 seeds/ha",
                    "considerations": [
                        "Ensure soil moisture is adequate",
                        "Consider using starter fertilizer",
                        "Check soil temperature at planting depth"
                    ]
                },
                "fertilization": {
                    "base_application": {
                        "npk_ratio": "15-15-15",
                        "timing": "Pre-planting or at planting",
                        "method": "Band placement 5cm below and beside seed"
                    },
                    "nitrogen_management": {
                        "total_n_required": "180-200 kg/ha",
                        "split_applications": [
                            "30% at planting",
                            "40% at V6 stage",
                            "30% at V12 stage"
                        ]
                    }
                },
                "irrigation": {
                    "critical_periods": [
                        "Early vegetative growth",
                        "Tasseling to silk emergence",
                        "Grain filling"
                    ],
                    "water_requirements": "500-800mm total",
                    "methods": [
                        "Center pivot irrigation",
                        "Drip irrigation for water conservation",
                        "Furrow irrigation in flat areas"
                    ],
                    "scheduling": {
                        "early_stage": "Light, frequent irrigation",
                        "mid_season": "Heavy irrigation during critical periods",
                        "late_season": "Reduced irrigation during maturity"
                    }
                }
            },
            CropType.WHEAT: {
                "soil_preparation": {
                    "tillage_depth": "15-20cm",
                    "primary_tillage": "Light cultivation for winter wheat",
                    "secondary_tillage": "Seedbed preparation",
                    "soil_requirements": {
                        "optimal_ph": "6.0-7.0",
                        "organic_matter": ">1.5%",
                        "drainage": "Moderate to well-drained",
                        "texture": "Medium to heavy soils preferred",
                        "compaction": "Avoid soil compaction below 15cm"
                    },
                    "seasonal_variations": {
                        "winter_wheat": {
                            "timing": "Early fall preparation",
                            "depth": "Slightly shallower to prevent heaving"
                        },
                        "spring_wheat": {
                            "timing": "Early spring as soon as workable",
                            "depth": "Standard depth for good root establishment"
                        }
                    },
                    "recommended_methods": [
                        "Minimum tillage for moisture conservation",
                        "No-till in suitable conditions",
                        "Conventional tillage in wet areas",
                        "Strip tillage for erosion control",
                        "Vertical tillage for residue management"
                    ]
                },
                "planting": {
                    "timing": {
                        "winter_wheat": "Early fall, 6 weeks before frost",
                        "spring_wheat": "Early spring, soil temp above 4°C"
                    },
                    "seed_depth": "3-5cm",
                    "row_spacing": "15-20cm",
                    "seeding_rate": "180-250 kg/ha",
                    "considerations": [
                        "Ensure good seed-to-soil contact",
                        "Plant winter wheat at proper depth for winter protection",
                        "Avoid planting too deep"
                    ]
                },
                "fertilization": {
                    "base_application": {
                        "npk_ratio": "18-46-0",
                        "timing": "At planting",
                        "method": "Drill with seed or broadcast"
                    },
                    "nitrogen_management": {
                        "total_n_required": "100-150 kg/ha",
                        "split_applications": [
                            "40% at planting",
                            "60% at tillering"
                        ]
                    }
                },
                "irrigation": {
                    "critical_periods": [
                        "Tillering",
                        "Stem elongation",
                        "Grain filling"
                    ],
                    "water_requirements": "450-650mm total",
                    "methods": [
                        "Sprinkler irrigation",
                        "Flood irrigation in level fields"
                    ],
                    "scheduling": {
                        "early_stage": "Regular light irrigation",
                        "mid_season": "Increased irrigation during heading",
                        "late_season": "Reduced irrigation during ripening"
                    }
                }
            }
        }

        # Add climate zone specific modifications
        climate_modifications = {
            "mediterranean": {
                "irrigation": {
                    "frequency": "Increased during dry season",
                    "water_conservation": "Critical consideration",
                    "methods": [
                        "Drip irrigation preferred",
                        "Night irrigation to reduce evaporation",
                        "Soil moisture monitoring essential"
                    ]
                },
                "planting": {
                    "timing": "Early spring for maximum rainfall utilization",
                    "varieties": "Drought-tolerant varieties recommended"
                },
                "soil_management": {
                    "mulching": "Recommended for moisture conservation",
                    "organic_matter": "Regular addition to improve water retention"
                }
            },
            "continental": {
                "planting": {
                    "timing": "Adjusted for shorter growing season",
                    "frost_protection": "Essential consideration",
                    "methods": [
                        "Use of frost-tolerant varieties",
                        "Row covers for early planting",
                        "Wind protection measures"
                    ]
                },
                "soil_preparation": {
                    "timing": "Early spring as soon as workable",
                    "methods": "Minimum tillage to preserve moisture"
                },
                "winter_protection": {
                    "methods": [
                        "Snow trapping techniques",
                        "Winter cover crops",
                        "Windbreaks"
                    ]
                }
            },
            "tropical": {
                "disease_management": {
                    "focus": "Increased focus on fungal disease prevention",
                    "methods": [
                        "Regular fungicide applications",
                        "Resistant varieties essential",
                        "Increased plant spacing for airflow"
                    ]
                },
                "irrigation": {
                    "focus": "Focus on drainage during wet season",
                    "methods": [
                        "Raised beds recommended",
                        "Surface drainage systems",
                        "Timing based on rainfall patterns"
                    ]
                },
                "soil_management": {
                    "erosion_control": "Critical in high rainfall",
                    "methods": [
                        "Contour plowing",
                        "Cover crops during rainy season",
                        "Terracing where appropriate"
                    ]
                }
            },
            "semi_arid": {
                "water_management": {
                    "conservation": "Absolute priority",
                    "methods": [
                        "Drought-resistant varieties",
                        "Mulching mandatory",
                        "Deep tillage for moisture retention"
                    ]
                },
                "soil_management": {
                    "focus": "Wind erosion control",
                    "methods": [
                        "Minimum tillage",
                        "Stubble retention",
                        "Windbreak establishment"
                    ]
                },
                "planting": {
                    "timing": "Synchronized with rainfall patterns",
                    "density": "Reduced for water conservation"
                }
            },
            "humid_subtropical": {
                "disease_management": {
                    "focus": "Year-round disease pressure",
                    "methods": [
                        "Resistant varieties",
                        "Preventive fungicide program",
                        "Cultural controls"
                    ]
                },
                "soil_management": {
                    "drainage": "Essential consideration",
                    "methods": [
                        "Raised beds",
                        "Subsurface drainage",
                        "Regular soil testing"
                    ]
                },
                "pest_management": {
                    "focus": "Year-round pest pressure",
                    "methods": [
                        "IPM strategies",
                        "Regular monitoring",
                        "Beneficial insect conservation"
                    ]
                }
            }
        }

        # Get base techniques for crop type
        techniques = base_techniques.get(crop_type, {})

        # Apply climate zone modifications if available
        if climate_zone.lower() in climate_modifications:
            climate_mods = climate_modifications[climate_zone.lower()]
            # Deep merge the modifications
            for key, value in climate_mods.items():
                if key in techniques:
                    techniques[key].update(value)
                else:
                    techniques[key] = value

        return techniques
