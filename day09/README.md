# Course Assignment Submission Analysis

A comprehensive analysis of student submission patterns for Python course assignments, revealing fascinating insights into learning behaviors and time management strategies.

## 📊 Key Findings

**Dataset Overview:**
- 📚 **8 assignments** analyzed (Day01-Day08)  
- 📝 **213 submissions** from **36 students**
- ⏰ **79.0 hours** average submission time before deadline
- 📅 **6.6%** late submissions (much better than expected!)
- 🏠 **43.7%** of work done on weekends

---

## 🎯 Visualizations

### 1. 🔥 Submission Heatmap
![Heatmap](plots/submission_heatmap.png)
**Peak activity:** Weekend evenings. Students clearly prefer personal time for coursework.
There is a nice amount of submissions just before the lecture time.

### 2. 👥 Student Personas: Early Birds vs Night Owls  
![Personas](plots/student_persona_scatter.png)
**Insight:** Most students are consistently early submitters! The scatter reveals distinct personas - some highly consistent, others more variable in their timing.

### 3. 🏃‍♂️ Submission Velocity by Assignment
![Velocity](plots/submission_velocity_ecdf.png)
**Pattern:** Each line shows how quickly students complete different assignments. Percentages show portion submitted by deadline - most assignments see 85-95% on-time completion!

### 4. ⚖️ Weekend Warriors vs Weekday Workers
![Weekend Warriors](plots/weekend_warrior_stacked_bar.png)
**Balance:** Students split work between weekdays (after hours) and weekends, with Weekend submissions being most popular for the majority.

### 5. ⏱️ Time Allocation Patterns
![Time Allocation](plots/time_allocation_patterns.png)
**Hypothesis Test:** Parkinson's Law - "work expands to fill the time available for its completion" 

Students consistently submit at approximately the same relative time point (around 85-95% through the assignment period) regardless of whether they have 3 days or 7 days to complete the work. Work indeed expands to fill the available time.