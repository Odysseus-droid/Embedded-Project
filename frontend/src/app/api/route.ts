import { NextRequest, NextResponse } from "next/server";
import { getRfids } from "@/backend/firebaseAdmin"; // adjust the path to your backend utility

export async function GET(req: NextRequest) {
  try {
    const data = await getRfids();
    return NextResponse.json(data);
  } catch (err) {
    return NextResponse.json({ error: "Failed to fetch RFIDs", details: err }, { status: 500 });
  }
}
