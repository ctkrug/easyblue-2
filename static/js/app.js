document.addEventListener("DOMContentLoaded", function() {
    // Get form elements
    const form = document.getElementById("filter-form");
    const sortBy = document.getElementById("sort_by");
    const sortOrder = document.getElementById("sort_order");
    const limit = document.getElementById("limit");
    const department = document.getElementById("category");
    const course_level = document.getElementById("course_level");
    const exclude_na = document.getElementById("exclude_na");
  
    // Load saved values from local storage, if available
    sortBy.value = localStorage.getItem("sortBy") || sortBy.value;
    sortOrder.value = localStorage.getItem("sortOrder") || sortOrder.value;
    limit.value = localStorage.getItem("limit") || limit.value;
    department.value = localStorage.getItem("department") || department.value;
    course_level.value = localStorage.getItem("course_level") || course_level.value;
    exclude_na.value = localStorage.getItem("exclude_na") || exclude_na.value;
  
    // Save values to local storage when form is submitted
    form.addEventListener("submit", function(event) {
      localStorage.setItem("sortBy", sortBy.value);
      localStorage.setItem("sortOrder", sortOrder.value);
      localStorage.setItem("limit", limit.value);
      localStorage.setItem("department", department.value);
      localStorage.setItem("course_level", course_level.value);
      localStorage.setItem("exclude_na", exclude_na.value);
    });
  });
  