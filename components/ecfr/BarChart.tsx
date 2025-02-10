"use client";

import React, { useState } from "react";
import * as Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import { BarChart as BarChartIcon, BarChartHorizontal } from "lucide-react";

// ecfr
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
interface BarChartProps extends HighchartsReact.Props {
	data: [string, number][];
	title: string;
	yAxisTitle: string;
}

export default function BarChart({
	data,
	title,
	yAxisTitle,
	...props
}: BarChartProps) {
	const [chartType, setChartType] = useState<"bar" | "column">("bar");

	const options: Highcharts.Options = {
		chart: {
			type: chartType,
			height: chartType === "bar" ? data.length * 30 : 800, // Adjust height based on type
			marginLeft: chartType === "bar" ? 300 : 100, // Adjust margin based on type
		},
		title: {
			text: title,
		},
		xAxis: {
			type: "category",
			title: {
				text: null,
			},
			labels: {
				style: {
					fontSize: "11px",
					fontFamily: "Verdana, sans-serif",
				},
				step: 0,
				maxStaggerLines: 1000,
				rotation: chartType === "column" ? -45 : 0, // Rotate labels for column view
			},
		},
		yAxis: {
			min: 0,
			title: {
				text: yAxisTitle,
				align: chartType === "bar" ? "high" : "middle",
			},
			labels: {
				overflow: "justify",
				formatter: function () {
					return Highcharts.numberFormat(this.value as number, 0, ",", ",");
				},
			},
			max: undefined,
		},
		legend: {
			enabled: false,
		},
		tooltip: {
			pointFormat: "Word Count: <b>{point.y:,.0f}</b>",
		},
		plotOptions: {
			bar: {
				dataLabels: {
					enabled: true,
					format: "{point.y:,.0f}",
					style: {
						fontSize: "11px",
						fontFamily: "Verdana, sans-serif",
					},
				},
				groupPadding: 0.1,
				pointPadding: 0.05,
			},
			column: {
				dataLabels: {
					enabled: true,
					format: "{point.y:,.0f}",
					style: {
						fontSize: "11px",
						fontFamily: "Verdana, sans-serif",
					},
					rotation: -90,
					y: 30,
				},
				groupPadding: 0.1,
				pointPadding: 0.05,
			},
			series: {
				turboThreshold: 0,
				animation: false,
			},
		},
		series: [
			{
				name: "Word Count",
				colorByPoint: true,
				data: data,
			} as any,
		],
		credits: {
			enabled: false,
		},
		boost: {
			enabled: false,
		},
	};

	return (
		<div className="w-full">
			<div className="mb-4">
				<ToggleGroup
					type="single"
					defaultValue="bar"
					value={chartType}
					onValueChange={(value) => {
						if (value) setChartType(value as "bar" | "column");
					}}
				>
					<ToggleGroupItem value="bar" aria-label="Horizontal View">
						<BarChartHorizontal className="h-4 w-4" />
						<span className="ml-2">Horizontal</span>
					</ToggleGroupItem>
					<ToggleGroupItem value="column" aria-label="Vertical View">
						<BarChartIcon className="h-4 w-4" />
						<span className="ml-2">Vertical</span>
					</ToggleGroupItem>
				</ToggleGroup>
			</div>
			<div
				className="w-full"
				style={{
					height: chartType === "bar" ? `${data.length * 30}px` : "800px",
					overflowY: chartType === "bar" ? "auto" : "hidden",
					overflowX: chartType === "column" ? "auto" : "hidden",
				}}
			>
				<HighchartsReact highcharts={Highcharts} options={options} {...props} />
			</div>
		</div>
	);
}

export { BarChart };
