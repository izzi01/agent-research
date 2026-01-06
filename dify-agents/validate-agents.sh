#!/bin/bash

# Validate Dify Agent YAML Files
# Checks for common import errors before uploading to Dify

echo "🔍 Validating Dify Agent Files..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Check if files exist
FILES=(
    "01-trend-monitor-agent.yml"
    "02-content-strategist-agent.yml"
    "03-text-creator-agent.yml"
    "04-approval-ui-agent.yml"
)

echo "📁 Checking file existence..."
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅${NC} Found: $file"
    else
        echo -e "${RED}❌${NC} Missing: $file"
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# Check for hardcoded variable IDs (should NOT exist)
echo "🔎 Checking for hardcoded variable IDs..."
if grep -r "#[0-9]\{10,\}\." *.yml > /dev/null 2>&1; then
    echo -e "${RED}❌ Found hardcoded timestamp IDs:${NC}"
    grep -n "#[0-9]\{10,\}\." *.yml
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅${NC} No hardcoded variable IDs found"
fi
echo ""

# Check for dynamic variable references (SHOULD exist)
echo "🔎 Checking for dynamic variable references..."
FOUND_VARS=0

if grep "{{product_categories}}" 01-trend-monitor-agent.yml > /dev/null; then
    echo -e "${GREEN}✅${NC} TrendMonitor: {{product_categories}} found"
    FOUND_VARS=$((FOUND_VARS + 1))
fi

if grep "{{trend_hashtag}}" 02-content-strategist-agent.yml > /dev/null; then
    echo -e "${GREEN}✅${NC} ContentStrategist: {{trend_hashtag}} found"
    FOUND_VARS=$((FOUND_VARS + 1))
fi

if grep "{{platform}}" 03-text-creator-agent.yml > /dev/null; then
    echo -e "${GREEN}✅${NC} TextCreator: {{platform}} found"
    FOUND_VARS=$((FOUND_VARS + 1))
fi

if [ $FOUND_VARS -eq 3 ]; then
    echo -e "${GREEN}✅${NC} All dynamic variables found"
else
    echo -e "${RED}❌${NC} Missing some dynamic variables"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Check YAML syntax (if Python + yaml module available)
if command -v python3 &> /dev/null; then
    if python3 -c "import yaml" 2>/dev/null; then
        echo "🔎 Validating YAML syntax..."
        for file in "${FILES[@]}"; do
            if [ -f "$file" ]; then
                if python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
                    echo -e "${GREEN}✅${NC} $file - Valid YAML"
                else
                    echo -e "${RED}❌${NC} $file - Invalid YAML syntax"
                    ERRORS=$((ERRORS + 1))
                fi
            fi
        done
    else
        echo -e "${YELLOW}⚠️${NC}  Python yaml module not installed, skipping YAML validation"
        echo "    (Install with: pip3 install pyyaml)"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${YELLOW}⚠️${NC}  Python3 not found, skipping YAML validation"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Check for required fields
echo "🔎 Checking required fields..."
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        MISSING=""
        
        grep -q "^version:" "$file" || MISSING="${MISSING}version, "
        grep -q "^kind:" "$file" || MISSING="${MISSING}kind, "
        grep -q "^app:" "$file" || MISSING="${MISSING}app, "
        grep -q "^model_config:" "$file" || MISSING="${MISSING}model_config, "
        grep -q "^tools:" "$file" || MISSING="${MISSING}tools, "
        
        if [ -z "$MISSING" ]; then
            echo -e "${GREEN}✅${NC} $file - All required fields present"
        else
            echo -e "${RED}❌${NC} $file - Missing: $MISSING"
            ERRORS=$((ERRORS + 1))
        fi
    fi
done
echo ""

# Check DSL version
echo "🔎 Checking DSL version..."
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        VERSION=$(grep "^version:" "$file" | awk '{print $2}')
        if [ "$VERSION" == "0.1.3" ]; then
            echo -e "${GREEN}✅${NC} $file - Version: $VERSION"
        else
            echo -e "${YELLOW}⚠️${NC}  $file - Version: $VERSION (expected 0.1.3)"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
done
echo ""

# Check backend URLs
echo "🔎 Checking backend URLs..."
if grep -q "host.docker.internal:8080" *.yml; then
    echo -e "${YELLOW}⚠️${NC}  Found Docker internal URL (host.docker.internal:8080)"
    echo "    Remember to update this to your actual backend URL after import"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}✅${NC} No Docker internal URLs found"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ VALIDATION PASSED${NC}"
    echo ""
    echo "All agents are ready to import into Dify!"
    echo ""
    echo "Next steps:"
    echo "1. Open Dify: http://localhost:3001"
    echo "2. Go to Studio → Create from DSL file"
    echo "3. Import each .yml file"
    echo "4. Update backend URLs in tools"
    echo "5. Test with suggested questions"
else
    echo -e "${RED}❌ VALIDATION FAILED${NC}"
    echo ""
    echo "Found $ERRORS error(s) and $WARNINGS warning(s)"
    echo "Please fix the errors before importing to Dify"
fi

if [ $WARNINGS -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}⚠️  $WARNINGS warning(s)${NC} - these won't prevent import but should be addressed"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Exit code
if [ $ERRORS -eq 0 ]; then
    exit 0
else
    exit 1
fi
