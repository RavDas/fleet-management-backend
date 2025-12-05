using System;

namespace VehicleService.Domain.Entities
{
    public class GeneratedReport
    {
        public int Id { get; set; }
        public string ReportName { get; set; } = string.Empty;
        public string ReportType { get; set; } = string.Empty;
        public DateTime GeneratedDate { get; set; }
        public string FileSize { get; set; } = string.Empty;
        public string Format { get; set; } = string.Empty;
        public string Data { get; set; } = string.Empty; // Store the JSON content
    }
}

