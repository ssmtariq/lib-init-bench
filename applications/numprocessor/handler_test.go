package main

import (
	"context"
	"testing"
)

func TestHandleRequest(t *testing.T) {
	tests := []struct {
		name    string
		req     Request
		want    float64
		wantErr bool
	}{
		{
			name: "multiply operation",
			req: Request{
				Operation: "multiply",
				Number:    10,
			},
			want:    20, // default multiplier is 2.0
			wantErr: false,
		},
		{
			name: "average operation",
			req: Request{
				Operation: "average",
			},
			want:    3, // average of [1,2,3,4,5]
			wantErr: false,
		},
		{
			name: "invalid operation",
			req: Request{
				Operation: "invalid",
				Number:    10,
			},
			want:    0,
			wantErr: true,
		},
	}

	ctx := context.Background()
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := handleRequest(ctx, tt.req)
			if (err != nil) != tt.wantErr {
				t.Errorf("handleRequest() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr && got.Result != tt.want {
				t.Errorf("handleRequest() = %v, want %v", got.Result, tt.want)
			}
		})
	}
}