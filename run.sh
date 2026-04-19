#!/usr/bin/env bash

echo ""
echo "  Hermes Runner"
echo "  ============="
echo ""
echo "  Available workflows:"
echo "    1. WF-01  Demand Signal Refresh"
echo "    2. WF-02  Supply Plan Generation"
echo "    3. WF-03  Protocol Amendment Impact"
echo "    4. WF-04  Routine Monitoring"
echo "    5. WF-05  Supply Plan Execution"
echo ""

read -p "  Enter workflow number (1-5): " WF
read -p "  Enter study ID: " STUDY
read -p "  Enter data drop date (YYYY-MM-DD, or press Enter for latest): " DROP

case "$WF" in
    1) WFID="WF-01" ;;
    2) WFID="WF-02" ;;
    3) WFID="WF-03" ;;
    4) WFID="WF-04" ;;
    5) WFID="WF-05" ;;
    *)
        echo ""
        echo "  ERROR: Invalid workflow number. Enter 1-5."
        exit 1
        ;;
esac

if [ -z "$STUDY" ]; then
    echo ""
    echo "  ERROR: Study ID is required."
    exit 1
fi

echo ""
echo "  Running $WFID for study $STUDY..."
echo ""

if [ -z "$DROP" ]; then
    python runner/runner.py --workflow "$WFID" --study "$STUDY"
else
    python runner/runner.py --workflow "$WFID" --study "$STUDY" --data-drop "$DROP"
fi
