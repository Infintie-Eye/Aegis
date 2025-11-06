class SafetyChecker:
    def __init__(self):
        self.crisis_keywords = {
            'high_risk': [
                'suicide', 'kill myself', 'end my life', 'want to die', 'better off dead',
                'take my own life', 'not worth living', 'end it all', 'overdose',
                'hurt myself', 'self harm', 'cut myself', 'harm myself'
            ],
            'moderate_risk': [
                'hopeless', 'worthless', 'give up', 'can\'t go on', 'no point',
                'nothing matters', 'waste of space', 'burden', 'everyone would be better off',
                'tired of living', 'want it to stop', 'can\'t take it anymore'
            ],
            'self_harm': [
                'cutting', 'self injury', 'burning myself', 'hitting myself',
                'self destructive', 'punish myself', 'hurt myself'
            ],
            'substance_abuse': [
                'drinking too much', 'using drugs', 'getting high to cope',
                'numbing the pain', 'drunk every day', 'can\'t stop drinking',
                'overdose', 'pills to feel better'
            ]
        }

        self.harmful_content_keywords = [
            'violence', 'revenge', 'hate', 'hurt others', 'make them pay',
            'get back at', 'they deserve to suffer'
        ]

        self.positive_indicators = [
            'getting help', 'therapy', 'counseling', 'support', 'friends',
            'family support', 'reaching out', 'talking to someone', 'professional help'
        ]

        # Pattern recognition for crisis escalation
        self.escalation_patterns = [
            r'(getting|feeling)\s+(worse|darker|hopeless)',
            r'(can\'t|cannot)\s+(take|handle|deal with)\s+it',
            r'(no\s+one|nobody)\s+(cares|understands|would miss me)',
            r'(planning|thinking about|considering)\s+(suicide|ending|hurting)'
        ]

    async def comprehensive_check(self, message: str) -> dict:
        """Comprehensive safety assessment of user message"""
        message_lower = message.lower()

        # Basic crisis detection
        basic_crisis = self.check(message)

        # Advanced pattern analysis
        pattern_analysis = await self._analyze_crisis_patterns(message_lower)

        # Severity assessment
        severity_score = await self._calculate_severity_score(message_lower, pattern_analysis)

        # Risk level determination
        risk_level = await self._determine_risk_level(severity_score, pattern_analysis)

        # Crisis indicators identification
        crisis_indicators = await self._identify_crisis_indicators(message_lower)

        # Protective factors identification
        protective_factors = await self._identify_protective_factors(message_lower)

        # Immediate intervention assessment
        immediate_intervention_needed = await self._assess_immediate_intervention(
            severity_score, pattern_analysis
        )

        return {
            'crisis_detected': basic_crisis['crisis_detected'],
            'crisis_level': severity_score,  # 0-10 scale
            'risk_level': risk_level,  # low, moderate, high, severe
            'crisis_indicators': crisis_indicators,
            'protective_factors': protective_factors,
            'harmful_content': basic_crisis['harmful_content'],
            'immediate_intervention_needed': immediate_intervention_needed,
            'safety_plan_required': severity_score >= 7,
            'professional_referral_urgent': severity_score >= 8,
            'emergency_services_consideration': severity_score >= 9,
            'pattern_analysis': pattern_analysis,
            'safe': severity_score < 5 and not basic_crisis['harmful_content']
        }

    def check(self, message: str) -> dict:
        """Basic safety check (maintaining compatibility)"""
        message_lower = message.lower()

        crisis_detected = any(
            keyword in message_lower
            for category in self.crisis_keywords.values()
            for keyword in category
        )

        harmful_content = any(keyword in message_lower for keyword in self.harmful_content_keywords)

        return {
            'crisis_detected': crisis_detected,
            'harmful_content': harmful_content,
            'safe': not (crisis_detected or harmful_content)
        }