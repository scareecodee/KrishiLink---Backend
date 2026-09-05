import math

class BuyerMatcher:
    def compute_match_score(self, listing, requirement) -> float:
        # Price compatibility (30%)
        price_diff = abs(listing.expected_price - requirement.budget_per_unit)
        price_score = max(0, 1 - (price_diff / requirement.budget_per_unit)) * 30

        # Quantity match (25%)
        min_qty = min(listing.quantity, requirement.quantity)
        max_qty = max(listing.quantity, requirement.quantity)
        qty_score = (min_qty / max_qty) * 25

        # Distance score (20%)
        # Default to 0 distance if coordinates missing
        distance_km = 0
        if listing.latitude and listing.longitude and requirement.radius_km:
            # Assuming requirement buyer lat/lon are handled before calling this, but for simplicity:
            pass # we'd calculate real distance. Mocking here.
            distance_km = 10 # mock distance
        
        rad = requirement.radius_km or 100
        dist_score = max(0, 1 - (distance_km / rad)) * 20

        # Quality match (25%)
        quality_score = 25.0
        if listing.quality_grade and requirement.quality_grade:
            if listing.quality_grade != requirement.quality_grade:
                quality_score = 12.5

        total_score = price_score + qty_score + dist_score + quality_score
        return total_score

    def find_matches(self, listing, requirements) -> list:
        matches = []
        for req in requirements:
            score = self.compute_match_score(listing, req)
            distance_km = 10.0 # Mock distance
            matches.append((req, score, distance_km))
        
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:10]

    def _calc_distance_km(self, lat1, lon1, lat2, lon2) -> float:
        if None in [lat1, lon1, lat2, lon2]:
            return 0.0
        R = 6371
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
