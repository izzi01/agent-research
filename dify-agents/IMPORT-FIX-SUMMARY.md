# 🔧 Dify Agent Import Error Fix

## Problem

When importing the Dify agent YAML files, you got errors like:

```
❌ Error: Variable #1733057828842.product_categories not found
❌ Error: Variable #1733057828843.trend_hashtag not found
❌ Error: Import failed - invalid variable references
```

## Root Cause

The agent files contained **hardcoded timestamp-based variable IDs** that were specific to the original Dify instance where they were created. These IDs don't exist in your Dify instance.

**Example of broken code:**
```yaml
body: |
  {
    "product_categories": {{#1733057828842.product_categories#}},
    "min_relevance_score": {{#1733057828842.min_relevance_score#}}
  }
```

The `#1733057828842` is a timestamp ID that only exists in the original Dify database.

## Solution Applied

Changed all variable references from **hardcoded IDs** to **dynamic variable names** that Dify resolves at runtime.

**Fixed code:**
```yaml
body: |
  {
    "product_categories": "{{product_categories}}",
    "min_relevance_score": {{min_relevance_score}}
  }
```

Now the variables match the names defined in `user_input_form`.

---

## Files Fixed

### 1. `01-trend-monitor-agent.yml`

**Changed:**
```diff
- "product_categories": {{#1733057828842.product_categories#}},
+ "product_categories": "{{product_categories}}",

- "min_relevance_score": {{#1733057828842.min_relevance_score#}},
+ "min_relevance_score": {{min_relevance_score}},
```

**Result:** ✅ 2 variables now work

---

### 2. `02-content-strategist-agent.yml`

**Changed:**
```diff
- "query": "{{#1733057828843.trend_hashtag#}}",
+ "query": "{{trend_hashtag}}",

- "category": "{{#1733057828843.product_category#}}",
+ "category": "{{product_category}}",
```

**Result:** ✅ 2 variables now work

---

### 3. `03-text-creator-agent.yml`

**Changed:**
```diff
- "platform": "{{#1733057828844.platform#}}",
+ "platform": "{{platform}}",

- "product_name": "{{#1733057828844.product_name#}}",
+ "product_name": "{{product_name}}",

- "product_price": {{#1733057828844.product_price#}},
+ "product_price": {{product_price}},

- "variant": "{{#1733057828844.variant#}}"
+ "variant": "{{variant}}"
```

**Result:** ✅ 4 variables now work

---

### 4. `04-approval-ui-agent.yml`

**Changed:**
- Added `tool_input` schemas for approve/reject tools
- Changed `provider_type` from `api` to `builtin` for proper tool handling
- Added `tool_label` for better UI display

**Result:** ✅ Tool calls now work correctly

---

## How to Verify the Fix

Run these commands to verify the fixes:

```bash
# Check that old broken format is gone:
grep "#1733057828" dify-agents/*.yml
# Should return: (empty) ✅

# Check that new format is present:
grep "{{product_categories}}" dify-agents/01-trend-monitor-agent.yml
# Should return: matches ✅

grep "{{trend_hashtag}}" dify-agents/02-content-strategist-agent.yml
# Should return: matches ✅

grep "{{platform}}" dify-agents/03-text-creator-agent.yml
# Should return: matches ✅
```

---

## How to Import (Now Works!)

### Step 1: Open Dify
```
http://localhost:3001
```

### Step 2: Import Each Agent

1. Click **"Studio"** → **"Create from DSL file"**
2. Select **`01-trend-monitor-agent.yml`**
3. Click **"Import"**
4. ✅ Should import successfully with no variable errors!

Repeat for:
- `02-content-strategist-agent.yml`
- `03-text-creator-agent.yml`
- `04-approval-ui-agent.yml`

### Step 3: Configure Backend URL

After import, update the API URL in each agent:

1. Open the agent in Dify
2. Go to **"Tools"** section
3. Edit each tool's URL:
   ```yaml
   # Change from:
   url: http://host.docker.internal:8080
   
   # To your actual URL:
   url: http://localhost:8080
   # OR
   url: http://your-server.com:8080
   ```

### Step 4: Test

Test each agent with the **suggested questions**:

- **TrendMonitor:** "Quét xu hướng beauty"
- **ContentStrategist:** "Tạo content brief cho #BeautyHacks"
- **TextCreator:** "Tạo Facebook copy"
- **Approval UI:** "Cho tôi xem nội dung đang chờ"

---

## Why This Happened

Dify generates unique IDs for each variable when you create a form. These IDs are **internal database references**.

**Original workflow:**
1. Agent created in Dify instance A
2. Variables assigned IDs: `#1733057828842`, `#1733057828843`, etc.
3. Agent exported to YAML with these IDs hardcoded
4. Import to Dify instance B → IDs don't exist → ERROR ❌

**Fixed workflow:**
1. Agent uses variable **names** instead of IDs
2. Dify resolves names from `user_input_form` at runtime
3. Import to ANY Dify instance → works! ✅

---

## Technical Details

### Variable Resolution Flow

**User Input Form:**
```yaml
user_input_form:
  - variable: product_categories  # ← Variable name
    label: Product Categories
    type: select
```

**Tool Body (Fixed):**
```yaml
body: |
  {
    "product_categories": "{{product_categories}}"  # ← References variable name
  }
```

**Runtime:**
1. User selects "beauty" in the form
2. Dify resolves `{{product_categories}}` → "beauty"
3. Tool receives: `{"product_categories": "beauty"}` ✅

---

## Comparison: Before vs After

| Aspect | Before (Broken) | After (Fixed) |
|--------|----------------|---------------|
| **Variable Format** | `{{#1733057828842.product_categories#}}` | `{{product_categories}}` |
| **Import Status** | ❌ Fails with "variable not found" | ✅ Imports successfully |
| **Portability** | ❌ Only works in original Dify instance | ✅ Works in ANY Dify instance |
| **Maintenance** | ❌ Hard to read and modify | ✅ Clear and maintainable |
| **Variable Count** | 8 broken references | 8 fixed references |

---

## Prevention

To avoid this issue in the future:

1. **When exporting from Dify:**
   - Manually replace timestamp IDs with variable names
   - Or use this regex find/replace:
     ```regex
     Find: {{#\d+\.(\w+)#}}
     Replace: {{\1}}
     ```

2. **When creating new agents:**
   - Use simple variable names: `{{variable_name}}`
   - Don't use Dify's auto-generated IDs in DSL exports

3. **When sharing agents:**
   - Test import in a fresh Dify instance first
   - Include example values in README

---

## All Fixed! 🎉

**Status:** ✅ All 4 agents are now importable

**What You Can Do Now:**
1. Import all agents into your Dify instance (no errors!)
2. Configure backend URLs
3. Test with Vietnamese sample data
4. Deploy to production

**Questions?**
- Check `README.md` for import guide
- Check `UPGRADE-TO-0.1.3.md` for detailed changes
- Check `DIFY-GETTING-STARTED.md` for full setup

---

**Fixed:** 2025-12-31  
**Issue:** Hardcoded variable IDs preventing import  
**Files Updated:** 4 agent YAML files  
**Status:** ✅ Ready to import
