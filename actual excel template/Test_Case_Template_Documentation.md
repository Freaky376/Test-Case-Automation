# Test Case Template Documentation

**File**: Test_Case_Template.xlsx  
**Location**: /home/jhoncb/My-Playground/  
**Last Analyzed**: 2026-02-10

---

## 📋 Template Structure

This Excel template contains **11 columns** for comprehensive test case documentation:

| Column | Field Name | Description |
|--------|------------|-------------|
| A | TestCase ID | Unique identifier for each test case |
| B | Priority | Test case priority level (dropdown: Critical, High, Medium, Low) |
| C | Title | Test case title/description |
| D | Precondition | Prerequisites needed before testing |
| E | Steps to Reproduce | Detailed steps to execute the test |
| F | Expected Results | What should happen when test is executed |
| G | Actual Result | What actually happened during testing |
| H | Acceptance Criteria | Designer-provided acceptance criteria for the test case |
| I | Status (Pass/Fail) | Test outcome (dropdown: Pass, Fail) |
| J | QA Tester | Person who executed the test |
| K | QA Notes | Additional notes or observations |

---

## 🔽 Dropdown Menus (Data Validation)

The template includes **2 automated dropdown menus**:

### 1. Priority Column (B)
- **Type**: List dropdown
- **Range**: Entire column B (rows 1-1,048,576)
- **Options**: 
  - Critical
  - High
  - Medium
  - Low

### 2. Status Column (I)
- **Type**: List dropdown
- **Range**: Entire column I (rows 1-1,048,576)
- **Options**:
  - Pass
  - Fail

---

## 🎨 Conditional Formatting & Color Coding

The template uses **automatic color coding** based on dropdown selections:

### Priority Column (B) - Color Scheme

| Priority | Color | Hex Code |
|----------|-------|----------|
| Critical | 🔴 Red | #FF4F4F |
| High | 🟠 Orange | #F9992F |
| Medium | 🟡 Yellow | #F4CE2C |
| Low | 🟢 Green | #77C38B |

### Status Column (I) - Color Scheme

| Status | Color | Hex Code |
|--------|-------|----------|
| Pass | 🟢 Green | #77C38B |
| Fail | 🔴 Red | #FF4F4F |

---

## ✨ Additional Features

- ✅ **Text Wrapping**: Enabled for multi-line content (especially useful for Steps to Reproduce)
- ✅ **Conditional Formatting**: Colors automatically apply when dropdown options are selected
- ✅ **Consistent Color Scheme**: Green = success/low priority, Red = failure/critical
- ✅ **Scalable**: Template ready for up to 1,048,576 rows
- ✅ **Professional Layout**: Clean, enterprise-ready design

---

## 📝 Sample Test Case Included

The template includes one complete example:

**TestCase ID**: 20262SP1-0001  
**Priority**: Critical  
**Title**: Verify display of Events in Detection module  
**Precondition**: Environment must have a Malware or Malicious Activity  
**Steps to Reproduce**:
```
1. Log in to the EDR Aquila module.
2. Navigate to the Cyber Monitoring > Endpoint Detection and Response (EDR) > Detection.
4. Select Events tab.
3. Review Event list.
```
**Expected Results**: Detection alerts are displayed with correct severity, timestamp, and endpoint details.  
**Status**: Fail

Additional rows (3-5) show example priority levels: High, Medium, Low

---

## 💡 Usage Recommendations

1. **TestCase ID Format**: Use consistent naming convention (e.g., `20262SP1-0001`, `PROJECT-0001`)
2. **Priority Assignment**: Set priority based on business impact and risk
3. **Steps Clarity**: Write clear, numbered steps that anyone can follow
4. **Expected Results**: Be specific about what constitutes a pass
5. **Actual Results**: Document exactly what happened, including environment details if test failed

---

## 🔧 Technical Details

- **File Format**: XLSX (Excel 2007+)
- **Sheet Name**: Page1
- **Dimensions**: 5 rows × 11 columns (with sample data)
- **Font**: Aptos Narrow, 11pt
- **Data Validation**: Applied to entire columns for scalability
- **Conditional Formatting Rules**: 6 format rules total (4 for Priority, 2 for Status)

---

## 📌 Notes

This template is designed for QA test case management and integrates well with:
- Manual testing workflows
- Test case generation scripts
- Bug reporting processes
- Automated test documentation

The color-coded priorities and statuses allow for quick visual scanning of test results and critical issues.
