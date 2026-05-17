# Database Schema

## User
Custom Django user with email login, password hashing, role, verification, avatar, and contact metadata.

## BrandProfile
One-to-one with User. Stores company name, industry, location, website, description, and monthly budget.

## InfluencerProfile
One-to-one with User. Stores niche, location, portfolio, social links, followers, engagement, demographics, pricing, verification, fake follower score, and sentiment score.

## Campaign
Belongs to a BrandProfile. Stores title, description, niche, budget, dates, status, deliverables, target locations, and predicted ROI.

## CampaignInvitation
Connects Campaign and InfluencerProfile. Stores invitation status, proposed rate, response timestamp, and submitted content details.

## Message
Connects sender, recipient, and optionally campaign. Supports attachments and read state.

## Notification
Belongs to a User. Stores notification type, title, body, read state, and creation time.

## Analytics
Belongs to a Campaign and optionally InfluencerProfile. Stores impressions, clicks, conversions, spend, revenue, engagement, sentiment, and calculated ROI.

## Payment
Belongs to Campaign and InfluencerProfile. Tracks amount, payment status, transaction reference, and payment date.

## Review
Connects reviewer, Campaign, and InfluencerProfile with a 1-5 rating and comment.
