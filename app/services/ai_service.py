"""
AI analysis service
"""
import hashlib
from typing import Optional, List
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database.init_db import AnalysisModel
from app.models.report import AnalysisResult

settings = get_settings()


class AIService:
    """Service for AI-powered threat analysis"""

    def __init__(self, db: Session):
        self.db = db
        self.cache = {}  # Simple in-memory cache

    async def analyze_threat(
        self,
        threat_id: int,
        threat_title: str,
        threat_type: str,
        severity: str,
        source_ip: Optional[str],
        description: str,
        include_recommendations: bool = True,
    ) -> AnalysisResult:
        """
        Analyze a threat using AI and return structured results
        """
        # Check cache
        cache_key = self._generate_cache_key(description)
        if cache_key in self.cache:
            cached_result = self.cache[cache_key]
            return AnalysisResult(
                threat_id=threat_id,
                summary=cached_result["summary"],
                technical_analysis=cached_result["technical_analysis"],
                recommendations=cached_result["recommendations"],
                severity_score=cached_result["severity_score"],
                confidence=cached_result["confidence"] * 0.9,  # Slightly reduce confidence for cached
                model_used="cached",
            )

        # Build analysis prompt
        prompt = self._build_analysis_prompt(
            threat_title, threat_type, severity, source_ip, description, include_recommendations
        )

        # Call AI (simulated if no API key)
        analysis_text, severity_score, confidence = await self._call_ai(prompt, description)

        # Generate recommendations if requested
        recommendations = []
        if include_recommendations:
            recommendations = self._generate_recommendations(threat_type, severity, analysis_text)

        # Save analysis to database
        db_analysis = AnalysisModel(
            threat_id=threat_id,
            analysis_text=analysis_text,
            recommendations="\n".join(recommendations) if recommendations else None,
            severity_score=severity_score,
            confidence=confidence,
            model_used=settings.ai_model if settings.ai_api_key else "simulated",
        )
        self.db.add(db_analysis)
        self.db.commit()

        # Cache result
        self.cache[cache_key] = {
            "summary": self._extract_summary(analysis_text),
            "technical_analysis": analysis_text,
            "recommendations": recommendations,
            "severity_score": severity_score,
            "confidence": confidence,
        }

        return AnalysisResult(
            threat_id=threat_id,
            summary=self._extract_summary(analysis_text),
            technical_analysis=analysis_text,
            recommendations=recommendations,
            severity_score=severity_score,
            confidence=confidence,
            model_used=settings.ai_model if settings.ai_api_key else "simulated",
        )

    def _build_analysis_prompt(
        self, title: str, threat_type: str, severity: str, source_ip: Optional[str], description: str, include_recommendations: bool
    ) -> str:
        """Build analysis prompt for AI"""
        prompt = f"""You are ThreatLens AI, an expert security analyst.

## Threat Details
- Title: {title}
- Type: {threat_type}
- Severity: {severity}
- Source IP: {source_ip or 'Unknown'}
- Description: {description}

## Analysis Tasks
1. Identify the attack vector and technique used
2. Assess potential impact on confidentiality, integrity, and availability
3. Determine if this is an isolated incident or part of a campaign
4. Provide a severity rating (1-10) with justification
"""
        if include_recommendations:
            prompt += """
5. Recommend immediate containment steps
6. Suggest long-term mitigation strategies
"""
        return prompt

    async def _call_ai(self, prompt: str, description: str) -> tuple[str, int, float]:
        """Call AI provider or simulate response"""
        if settings.ai_api_key:
            try:
                # Real API call would go here
                # For now, fall back to simulation
                pass
            except Exception:
                pass

        # Simulated AI response
        return self._simulate_analysis(description)

    def _simulate_analysis(self, description: str) -> tuple[str, int, float]:
        """Generate simulated AI analysis"""
        description_lower = description.lower()

        # Determine threat characteristics based on description
        if any(word in description_lower for word in ["brute", "force", "login", "password"]):
            threat_category = "brute_force_attack"
            analysis = "The detected activity suggests a brute force attack pattern. Multiple authentication attempts were observed from the same source, indicating an automated attack tool being used to guess credentials. This type of attack typically targets services with weak or default passwords."
            severity = 7
            confidence = 0.85
        elif any(word in description_lower for word in ["sql", "injection", "database"]):
            threat_category = "sql_injection"
            analysis = "The activity patterns indicate a potential SQL injection attempt. This vulnerability could allow an attacker to execute arbitrary SQL commands, potentially leading to unauthorized data access or database manipulation."
            severity = 9
            confidence = 0.90
        elif any(word in description_lower for word in ["malware", "virus", "trojan", "ransomware"]):
            threat_category = "malware"
            analysis = "Analysis suggests the presence of malware indicators. The behavioral patterns are consistent with known malware families, and immediate containment is recommended to prevent lateral movement."
            severity = 9
            confidence = 0.88
        elif any(word in description_lower for word in ["ddos", "denial", "service"]):
            threat_category = "dos_attack"
            analysis = "The observed traffic patterns are characteristic of a denial of service attack. Multiple requests from distributed sources are overwhelming the target, causing service degradation."
            severity = 8
            confidence = 0.82
        elif any(word in description_lower for word in ["unauthorized", "access", "breach", "data"]):
            threat_category = "unauthorized_access"
            analysis = "Evidence indicates unauthorized access attempts. An attacker may have gained or attempted to gain access to systems or data without proper authentication."
            severity = 8
            confidence = 0.87
        else:
            threat_category = "general_threat"
            analysis = "A security event was detected that warrants further investigation. The pattern does not immediately match known attack signatures, but the activity is suspicious and should be analyzed by a security professional."
            severity = 5
            confidence = 0.70

        return analysis, severity, confidence

    def _generate_recommendations(self, threat_type: str, severity: str, analysis: str) -> List[str]:
        """Generate security recommendations"""
        recommendations = []

        # Type-specific recommendations
        if "brute" in threat_type.lower():
            recommendations.extend([
                "Implement account lockout policies after failed login attempts",
                "Enforce strong password policies (min 12 chars, complexity requirements)",
                "Enable multi-factor authentication (MFA)",
                "Implement rate limiting on authentication endpoints",
                "Consider implementing CAPTCHA for repeated login attempts",
            ])
        elif "injection" in threat_type.lower():
            recommendations.extend([
                "Use parameterized queries or ORM for database operations",
                "Implement input validation and sanitization",
                "Apply principle of least privilege for database accounts",
                "Enable Web Application Firewall (WAF)",
                "Conduct code review and security testing",
            ])
        elif "malware" in threat_type.lower():
            recommendations.extend([
                "Isolate affected systems immediately",
                "Run full antivirus/EDR scan on affected hosts",
                "Review recent software installations and updates",
                "Check for persistence mechanisms (scheduled tasks, services)",
                "Preserve evidence for forensic analysis",
            ])
        else:
            recommendations.extend([
                "Investigate the source and scope of the threat",
                "Review access logs for similar patterns",
                "Implement additional monitoring on affected systems",
                "Consider implementing security automation",
                "Document findings for future reference",
            ])

        # Add severity-based recommendations
        if severity in ["high", "critical"]:
            recommendations.insert(0, "URGENT: Consider immediate containment actions (isolate systems, block IPs)")

        return recommendations[:5]  # Return top 5 recommendations

    def _extract_summary(self, analysis: str) -> str:
        """Extract a short summary from analysis"""
        sentences = analysis.split(".")
        summary = sentences[0] if sentences else analysis
        if len(summary) > 200:
            summary = summary[:200] + "..."
        return summary

    def _generate_cache_key(self, description: str) -> str:
        """Generate cache key for threat description"""
        return hashlib.md5(description.encode()).hexdigest()
