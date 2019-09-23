{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "project.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "project.fullname" -}}
{{- $name := .Chart.Name -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" $name .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "project.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "project.labels" -}}
{{- $version := default .Chart.AppVersion .Values.version -}}
app: {{ include "project.name" . }}
{{ if .Values.environment }}
environment: {{ .Values.environment }}
{{ end -}}
version: {{ $version | quote }} 
app.kubernetes.io/name: {{ include "project.name" . | quote }}
app.kubernetes.io/instance: {{ .Release.Name | quote }}
app.kubernetes.io/version: {{ $version | quote }} 
app.kubernetes.io/managed-by: {{ .Release.Service | quote }}
helm.sh/chart: {{ include "project.chart" . }}
{{- end -}}

{{/*
Common selector
*/}}
{{- define "project.selector" -}}
app.kubernetes.io/name: {{ include "project.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Define the ELB DNS for our environments
*/}}
{{- define "project.tls.dns" -}}
{{- if .Values.ingress.production -}}
{{- print "a9807e735a24111e9ae3a0652db2474f-1543514430.eu-west-1.elb.amazonaws.com" -}}
{{- else -}}
{{- print "a59504149a2ec11e9b079069e4c7fa15-2077560240.eu-west-1.elb.amazonaws.com" -}}
{{- end -}}
{{- end -}}

{{/*
Define the host for our environments
*/}}
{{- define "project.tls.host" -}}
{{- $name := (.Chart.Name | trunc 63 | trimSuffix "-") -}}
 {{- if .Values.ingress.host -}}
  {{- .Values.ingress.host -}}
 {{- else -}}
  {{- if .Values.ingress.subdomain -}}
   {{- printf "%s.%s" .Values.ingress.subdomain "app.debarrage.org" -}}
  {{- else -}}
   {{- printf "%s.%s" $name "app.debarrage.org" -}}
  {{- end -}}
 {{- end -}}
{{- end -}}